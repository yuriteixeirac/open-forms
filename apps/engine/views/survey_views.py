from django.shortcuts import render, get_object_or_404
from django.db.models import BooleanField, Count
from django.db.models.expressions import Case, When
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from apps.api.models import Survey, Submission

@login_required
def survey_creation(request):
    return render(request, 'engine/survey-creation.html')


@login_required
def survey_visualization(request, pk: int | None = None):
    survey = get_object_or_404(Survey, pk=pk)
    return render(request, 'engine/survey-visualization.html', {
        'survey': survey
    })


@login_required
def dashboard(request):
    surveys = Survey.objects.filter(owner=request.user).annotate(   # type: ignore
        submission_count=Count('submission'),
        is_active=Case(
            When(valid_until__gt=now(), then=True),
            default=False,
            output_field=BooleanField()
        )
    )
    recent_submissions = Submission.objects.filter(     # type: ignore
        survey__owner=request.user
    ).order_by('-created_at')[:15]

    return render(request, 'engine/dashboard.html', {
        'stats': {
            'total_surveys':      surveys.count(),
            'active_surveys':     surveys.filter(is_active=True).count(),
            'total_submissions':    Submission.objects.filter(survey__owner=request.user).count(),  # type: ignore
            'submissions_this_week': Submission.objects.filter(     # type: ignore
                survey__owner=request.user,
                created_at__gte=now() - timedelta(weeks=1)  # was answered_at
            ).count()
        },
        'surveys': surveys.order_by('-is_active', '-created_at'),
        'recent_submissions': recent_submissions,
    })


@login_required
def survey_detail(request, pk: int | None):
    survey = get_object_or_404(Survey, pk=pk, owner=request.user)
    submissions = Submission.objects.filter(survey=survey).order_by('-created_at')
    submission_count = submissions.count()

    # ── Build a lookup: question_id → all answers received ──────
    answers_by_question = {}
    for submission in submissions:
        for answer in submission.answers:
            qid = answer['question_id']
            if qid not in answers_by_question:
                answers_by_question[qid] = []
            answers_by_question[qid].append(answer['value'])

    # ── Enrich each question with aggregated answer data ─────────
    questions_data = []
    for question in survey.questions:
        qid       = question['id']
        qtype     = question['type']
        raw       = answers_by_question.get(qid, [])
        responded = len([v for v in raw if v is not None and v != '' and v != []])

        entry = {
            'id':        qid,
            'question':  question['question'],
            'type':      qtype,
            'required':  question.get('required', False),
            'responded': responded,
        }

        if qtype in ('radio', 'checkbox'):
            counts = {}
            for options in question.get('options', []):
                counts[options] = 0
            for value in raw:
                items = value if isinstance(value, list) else [value]
                for item in items:
                    if item in counts:
                        counts[item] = counts[item] + 1

            total = sum(counts.values()) or 1   # avoid div/0
            entry['option_stats'] = [
                {
                    'label': label,
                    'count': count,
                    'pct':   round(count / total * 100),
                }
                for label, count in counts.items()
            ]

        elif qtype == 'text':
            entry['text_answers'] = [v for v in raw if v]

        elif qtype == 'number':
            numbers = [v for v in raw if v is not None]
            entry['number_answers'] = numbers
            entry['average'] = round(sum(numbers) / len(numbers), 2) if numbers else None
            entry['minimum'] = min(numbers) if numbers else None
            entry['maximum'] = max(numbers) if numbers else None

        questions_data.append(entry)

    return render(request, 'engine/survey-detail.html', {
        'survey':           survey,
        'submission_count': submission_count,
        'recent_submissions': submissions[:10],
        'questions_data':   questions_data,
    })
