def lesson(id, chapter, title, subtitle, pages):
    return {"id": id, "chapter": chapter, "title": title, "subtitle": subtitle, "pages": pages}

def theory(title, text):
    return {"type": "theory", "title": title, "text": text}

def code(title, code_text, note=""):
    return {"type": "code", "title": title, "code": code_text, "note": note}

def quiz(question, options, answer, explain=""):
    return {"type": "quiz", "question": question, "options": options, "answer": answer, "explain": explain}

def practice(task, template, answers, hint="", explain=""):
    return {"type": "practice", "task": task, "template": template, "answers": answers, "hint": hint, "explain": explain}