import app
import requests
from flask import Blueprint
from flask import render_template, request
from flask.ext.login import login_required

from bs4 import BeautifulSoup

from app.exceptions import *

mod = Blueprint('quora', __name__)

@mod.route('/', methods=["GET"])
@login_required
def index():
    return render_template('quora_index.html')


@mod.route('/process', methods=["GET"])
def process():
    profile_page_url = request.args.get('url')
    if not profile_page_url:
        return render_template('quora-widget/error.html', \
                error='Invalid Profile URL : ' + profile_page_url)

    quora_profile = requests.get(profile_page_url)

    if quora_profile.status_code != 200:
        return render_template('quora-widget/error.html', \
                error=quora_profile.text)

    answers_page_url = profile_page_url.strip('/') + '/answers'

    soup = BeautifulSoup(quora_profile.text, 'html.parser')

    # Profile Info
    html_profile_info = soup.find(attrs={'class': 'ProfileNameAndSig'})

    profile_pic = soup.find(attrs={'class': 'profile_photo_img'}).get('data-src')
    profile_name = html_profile_info.find('h1').text.strip()
    try:
        profile_bio = html_profile_info.find(attrs={'class': 'rendered_qtext'})\
            .text.strip()
    except:
        profile_bio = None

    profile_info = {
        'name': profile_name,
        'bio': profile_bio,
        'img': profile_pic,
        'link': profile_page_url
    }

    # Highlights
    highlights = []

    html_highlights_info = soup.find(attrs={'class': 'Highlights'})
    if html_highlights_info:
        html_highlights = html_highlights_info.findAll('div', recursive=False)

        for html_highlight in html_highlights:
            highlights.append({
                    'title': html_highlight.find(attrs={'class': 'title'})\
                            .text.strip(),
                    'detail': html_highlight.find(attrs={'class': 'detail'})\
                            .text.strip()
            })

    # Stats
    stats = []
    html_stats_info = soup.findAll(attrs={'class':'stat'})

    for html_stat in html_stats_info:
        stats.append({
            'title': html_stat.find(attrs={'class': 'stat_label'})\
                    .text.strip(),
            'detail': html_stat.find(attrs={'class': 'total_count'})\
                    .text.strip()
        })

    # Primary Stats
    count_answers = soup.find(attrs={'class': 'AnswersNavItem'})\
                        .find('span').text.strip()
    count_followers = soup.find(attrs={'class': 'FollowersNavItem'})\
                        .find('span').text.strip()

    # Fetch Answers Page
    quora_answers = requests.get(answers_page_url)
    if quora_answers.status_code != 200:
        return render_template('quora-widget/error.html', \
                error=quora_answers.text)

    soup = BeautifulSoup(quora_answers.text, 'html.parser')

    # Answers
    # answers = []
    # html_answers_info = soup.findAll(attrs={'class':'AnswerListItem'})
    #
    # for html_answer_info in html_answers_info:
    #     question_text = html_answer_info.find(attrs={'class': 'QuestionText'})\
    #             .text.strip()
    #
    #     question_link = html_answer_info.find(attrs={'class': 'QuestionText'})\
    #             .find(attrs={'class': 'question_link'}).get('href')
    #
    #     if not 'quora.com/' in question_link:
    #         question_link = 'https://www.quora.com' + question_link
    #
    #     html_answer_content = html_answer_info.find(attrs={'class': 'answer_content'})
    #
    #     print question_text
    #
    #     try:
    #         image_link = html_answer_content.find(attrs={'class': 'truncated_thumbnail_holder'}).find('img').get('master_src')
    #     except:
    #         image_link = None
    #
    #     answer_parts = []
    #     html_answer_parts = html_answer_content.findAll(attrs={'class': 'qtext_para'})
    #     for answer_part in html_answer_parts:
    #         answer_parts.append(answer_part.text.strip())
    #
    #     answers.append({
    #         'link': question_link,
    #         'question': question_text,
    #         'answer': {
    #             'img': image_link,
    #             'text': ' '.join(answer_parts)
    #         }
    #     })

    return render_template('quora-widget/card.html', \
            profile_info=profile_info, highlights=highlights, stats=stats, \
            count_answers=count_answers, count_followers=count_followers)

    # return render_template('quora-widget/widget.html', \
    #         profile_info=profile_info, highlights=highlights, stats=stats, \
    #         count_answers=count_answers, count_followers=count_followers,\
    #         answers=answers)
