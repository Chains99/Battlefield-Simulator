def register_keywords(lexical_analizer, keywords):
    for keyword in keywords:
        lexical_analizer.register_keyword(keyword[0], keyword[1])


def register_operators(lexical_analizer, operators):
    for operator in operators:
        lexical_analizer.register_operator(operator[0], operator[1])


def register_texts(lexical_analizer, texts):
    for text in texts:
        lexical_analizer.register_text(text[0], text[1])

def register_comments(lexical_analizer, comments, allowLB):
    for comment in comments:
        lexical_analizer.register_comment(comment[0], comment[1])
