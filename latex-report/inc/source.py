# Подгружаем токенайзер по предложениям, TermExtractor и регулярки
from nltk import sent_tokenize
# import nltk
# nltk.download('punkt')
from rtm.rutermextract import TermExtractor
import re
from latex import escape


# Разбиение текста на параграфы
def handle_text(text):
    try:
        return "\n".join(transform_paragraph(p) for p in text.split("\n"))
    finally:
        close_downloader()


# Обработка параграфа
def transform_paragraph(p):
    image_pars = ""
    output_text = ""

    for sent in sent_tokenize(p, 'russian'):
        new_sent, latex = transform_sent(sent)
        output_text += new_sent + " "
        if latex:
            image_pars += "\n" + latex

    return output_text + image_pars


# Обработка предложения
unique_idx = 0  # лучше использовать UUID, но и это подойдет.

term_extractor = TermExtractor(ranker=lambda terms, weight: terms)


def transform_sent(sent):
    global unique_idx
    sent_terms = term_extractor(sent)
    if len(sent_terms) < 2 or not terms_contain_trigger(sent_terms):
        return sent, None

    img_file = "image%s" % str(unique_idx)
    unique_idx += 1

    context = extract_context(sent_terms)

    download_image(context, img_file)
    tex_text = create_tex_image(context, img_file)

    img_ref = "fig:%s" % img_file
    return insert_ref(sent, img_ref), tex_text


# Проверка, содержит ли список термов слово-триггер
def terms_contain_trigger(sent_terms):
    for term in sent_terms:
        if "рисунок" in term.normalized:
            return True
    return False


# Извлечение описания рисунка из списка термов
def extract_context(sent_terms):
    if "рисунок" in sent_terms[0].normalized:
        ret = sent_terms[1].normalized
        return ret

    for i in range(1, len(sent_terms)):
        if "рисунок" in sent_terms[i].normalized:
            ret = sent_terms[i - 1].normalized
            return ret

    raise Exception("здесь оказаться не должны")


# Вставка ссылки в предложение
def insert_ref(sent, img_ref):
    match = re.search(r"(рисун(ок|ке|ка))", sent, re.IGNORECASE)
    return sent[:match.end(0)] + " \\ref{%s}" % escape(img_ref) \
        + sent[match.end(0):]


# Вставка рисунка, используя $\LaTeX$ - макрос
def create_tex_image(context, img_file):
    return "\\insertimage{%s}{%s}" % (escape(img_file), context.capitalize())


# Загрузка картинок. Ее можно временно отключить при помощи `disable_dwnld`
disable_dwnld = False
if not disable_dwnld:
    from yaimages.yandex_images_download.downloader \
        import YandexImagesDownloader
    downloader = YandexImagesDownloader(output_directory="images/")


def download_image(context, img_file):
    if disable_dwnld:
        return
    downloader.download_images_by_keyword(context, img_file)


def close_downloader():
    if disable_dwnld:
        return
    downloader.driver.quit()


# Запуск программы
with open('input.txt', encoding="utf8") as f:
    text = handle_text(f.read())
    print(text)
    with open('output.tex', encoding="utf8", mode="w") as f:
        f.write(text)
