from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegisterForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Topic,Question,WrongAnswer
import random
def home(request):
    return render(request,'quizapp/home.html')

def register(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form=RegisterForm()
    return render(request,'quizapp/register.html',{'form':form})

def login_view(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():          
            login(request,form.user)
            return redirect('home')
    else:
        form=LoginForm()
    return render(request,'quizapp/login.html',{'form':form})

@login_required
def logout_view(request):
    # This will flush the session and log the user out:
    logout(request)
    print('logged out')
    # Redirect them somewhere sensible, e.g. your login page or home:
    return redirect('login')  

def topic_view(request):
    topics=Topic.objects.all()
    return render(request,'quizapp/topics.html',{'topics':topics})


"""
views req:
    1)start_quiz_view
    2)question_view
    3)result_view

1)start_quiz_view (request,topic_id):
        topic=get_object(Topic,id=topic_id)
        if request='GET':
            questions=list(Questions.objects.filter(topic=topic))

            random.sample(questions,5)

            create session['question id']=
            create session['score']=
        return redirect('question_view')
    return redirect('start_quiz_view')

2) question_view(request,):
        if ques (idx)>=5:
            redirect('result page')
        get the ques indx and display ques
       
        if req.method=='post':
            check if the ans is right(if yes):
                session['score']+=1
            else:
                store ques in db(wrong ans model)
        current index+=1
        return(question as context)

3)result_view(request):
        if request.method=='GET':
        total score=request.session.get('score')
        return (in result.html)
            
"""


def start_quiz_view(request,topic_id):
    request.session.pop('answered', None)
    request.session.pop('last_result', None)


    topic=get_object_or_404(Topic,id=topic_id)
    if request.method=='GET':
        all_questions=list(Question.objects.filter(topic=topic))
        No_of_questions=20
        generated_questions=random.sample(all_questions,No_of_questions)
        #create session and store : 
        request.session['questions_id']= [q.id for q in generated_questions]
        request.session['score']=0
        request.session['present_question']=0

        return redirect('question_view')
    return redirect('start_quiz')

def question_view(request):
    question_ids = request.session.get('questions_id', [])
    current_index = request.session.get('present_question', 0)

    if current_index >= len(question_ids):
        return redirect('result_view')

    question_id = question_ids[current_index]
    question = get_object_or_404(Question, id=question_id)

    show_explanation = False
    explanation = None
    selected_option = None
    is_correct = None
    answered = request.session.get('answered', False)

    if request.method == 'POST':
        if 'next' in request.POST:
            # Move to next question
            request.session['present_question'] = current_index + 1
            request.session['answered'] = False
            return redirect('question_view')

        selected_option = request.POST.get('option')
        if not answered:
            if selected_option == question.correct_option:
                request.session['score'] += 1
                is_correct = True
            else:
                is_correct = False
                WrongAnswer.objects.update_or_create(
                    user=request.user,
                    question=question,
                    defaults={'selected_option': selected_option}
                )
            explanation = question.explanation
            request.session['answered'] = True
            request.session['last_result'] = {
                'is_correct': is_correct,
                'explanation': explanation,
                'selected_option': selected_option,
            }

    if request.session.get('answered', False):
        show_explanation = True
        result_data = request.session.get('last_result', {})
        is_correct = result_data.get('is_correct')
        explanation = result_data.get('explanation')
        selected_option = result_data.get('selected_option')

    current_score = request.session.get('score', 0)

    return render(request, 'quizapp/questionlist.html', {
        'question': question,
        'explanation': explanation,
        'show_explanation': show_explanation,
        'selected_option': selected_option,
        'is_correct': is_correct,
        'current_index': current_index,
        'total_questions': len(question_ids),
        'score': current_score,
    })


def result_view(request):
    if request.method == 'GET':
        total_score = request.session.get('score', 0)  # default to 0 if not found
        return render(request, 'quizapp/result.html', {
            'total_score': total_score
        })


"""
review(request,pk):
    topic=get_obj_or_404(Topic, user_input)(gets topic object)
    model.objects.filter(Q(user=request.user)) & Q(question__topic=topic)
    return ({'ques':ques})


"""


def review_mistakes(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    ques = WrongAnswer.objects.filter(user=request.user, question__topic=topic)
    return render(request, 'quizapp/review.html', {'ques': ques, 'topic': topic})