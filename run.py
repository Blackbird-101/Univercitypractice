import os, sys

from app.utils import get_age_string, get_info_of_resumes, transliterate
project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_directory)

from app import create_app

app = create_app()

@app.context_processor
def utility_processor():
    return dict(int=int, str=str, all=all, 
                get_info_of_resumes=get_info_of_resumes,
                get_age_string=get_age_string,
                transliterate=transliterate)  # Делаем встроенные функции int, str доступными в шаблонах


if __name__ == "__main__":
    app.run(debug=True)