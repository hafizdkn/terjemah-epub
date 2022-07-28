from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup
from itertools import chain
from tqdm import tqdm
from lxml import html
import os

from utilities.read_config import ReadConfig


class GoTranslate:
    def __init__(self, list_target_file, config_path):
        self.sc_bs4 = ""
        self.sc_file = ""
        self.sc_lxml = ""
        self.config = ReadConfig(config_path)
        self.list_target_tag = None
        self.list_ignore_class = None
        self.list_ignore_tag = None
        self.config_path = config_path
        self.list_target_file = list_target_file

    def set_target_tag(self):
        res = self.config.get_value("Tag", "targetTag")
        self.list_target_tag = res

    def set_ignore_class_value(self):
        res = self.config.get_value("IgnoreClass", "ignoreClass")
        self.list_ignore_class = res

    def set_ignore_tag(self):
        res = self.config.get_value("SelfClosingTag", "selfClosingTag")
        self.list_ignore_tag = res

    def read_file(self, file):
        with open(file, "r") as f:
            return f.read()

    def get_name_file(self, file):
        return os.path.split(file)[-1]

    def get_length_file(self, file):
        return len(file)

    def join_text(self, text):
        return "".join(text)

    def split_text(self, text, split_char):
        new_text = text.split(split_char)
        return list(filter(lambda x: len(str(x)) != 0, new_text))

    def translate_text(self, text):
        if len(text) == 4 and text in ["None", "NONE", "none", None]:
            return text
        try:
            resp = GoogleTranslator(source="en", target="id").translate(text=text)
        except Exception:
            return text
        else:
            if resp != None:
                return resp
            return text

    def extract_element(self, element):
        # elements = (
        #     [element.text]
        #     + list(chain(*([] if c.tag in self.list_ignore_tag else [c.text, c.tail] for c in element.getchildren())))
        #     + [element.tail]
        # )
        # return list(filter(None, elements))
        return "".join(element.itertext()).strip()

    def parse_bs4(self, html_text):
        ignore_class = self.list_ignore_class
        target_tag = self.list_target_tag

        self.sc_bs4 = BeautifulSoup(html_text, "html.parser")
        elements = self.sc_bs4.find_all(
            target_tag, class_=lambda x: x not in ignore_class
        )
        return elements

    def parse_lxml(self, elements):
        return [html.fromstring(str(element)) for element in elements]

    def insert_new_js(self):
        body_tag = self.sc_bs4.find("body")
        script__min_js = self.sc_bs4.new_tag("script", attrs={"src": "./jquery.min.js"})
        script_js_event = """
        $('.div-class').click(function (event) {
            setTimeout(function () {
            var topic = event.target.innerText;
            $('summary').html(topic);
            }, 20);
        });
        """
        script_js = self.sc_bs4.new_tag("script")
        script_js.append(script_js_event)
        body_tag.insert_after(script_js)
        body_tag.insert_after(script__min_js)

    def insert_new_element(self, element=None, idx=None, status="ok"):
        if status == "ok":
            elm = self.sc_bs4_filtered[idx]
            soup = BeautifulSoup(str(elm), "html.parser")
            source = soup.find(elm.name)
            elm.clear()

            new_elm_dtls = soup.new_tag("div")
            new_elm_summary = soup.new_tag(
                "div",
                attrs={
                    "style": "display:inline;cursor:pointer;list-style:none;",
                },
            )
            new_elm_dtls.insert(0, new_elm_summary)
            new_elm_summary.insert(1, BeautifulSoup(str(element), "html.parser"))

            new_elm_dtls.append(new_elm_summary)

            ori_text = []
            for content in reversed(source.contents):
                ori_text.append(str(content.extract()))

            mark = soup.new_tag(
                "mark",
                attrs={
                    # "class": "div-class",
                    # "style": "background-color: rgb(173,216,230)",
                },
            )
            ori_text = "".join(reversed(ori_text))
            div_ = soup.new_tag("div")
            div_.insert(0, mark)
            mark.insert(1, BeautifulSoup(ori_text, "html.parser"))
            new_elm_dtls.append(div_)

            elm.insert(0, BeautifulSoup(str(new_elm_dtls), "html.parser"))

        else:
            elm = self.sc_bs4_filtered[idx]
            elm.insert(1, BeautifulSoup(element, "html.parser"))

    def run_parse(self, elements):
        self.insert_new_js()
        for idx, sc_lxml in enumerate(elements):
            tlist = self.extract_element(sc_lxml)
            t = "".join(tlist)
            if len(t.strip()) == 0:
                self.insert_new_element(element="", idx=idx, status="error")
                continue

            translated_text = self.translate_text(t)
            el = f'<span style="font-weight: 400;line-height:1.7rem; color: black;">{str(translated_text)}</span>'
            self.insert_new_element(el, idx)

    def write_to_file(self, name, file):
        with open(name, "w") as f:
            f.write(str(file))

    def run(self):
        self.set_ignore_class_value()
        self.set_target_tag()
        self.set_ignore_tag()

        total_file = self.get_length_file(self.list_target_file)
        print("\n[==] Total file          :", total_file)

        with tqdm(total=total_file) as pbar:
            for file in self.list_target_file:
                pbar.set_description(f"[..] Proses: {self.get_name_file(file)}")

                sc_html = self.read_file(file)
                self.sc_bs4_filtered = self.parse_bs4(sc_html)

                elements = self.parse_lxml(self.sc_bs4_filtered)
                self.run_parse(elements)

                self.write_to_file(file, self.sc_bs4)
                pbar.update(1)
