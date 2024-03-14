from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserRegistration, Feedback, AdminRegistration, Puzzle, PyStory, CStory, Profile
from django.db import IntegrityError
from django.contrib import messages
import openai, requests

openai.api_key ='#########################'

# Create your views here.

def code(request, language, puzzleid):
    if language == 'python3':
        level='plevel'
    elif language == 'c':
        level='clevel'
    else:
        level=''
    # Initialize context dictionary with language and puzzleid
    context = {"language": language, "puzzleid": puzzleid, "level":level}
    inp=None
    # Set default code value for the code editor textarea
    defcode = ""
    context['code'] = defcode
    
    try:
        # Attempt to retrieve puzzle from the database using puzzleid
        puzzle = Puzzle.objects.get(puzzleID=puzzleid)
        context["url"]=puzzle.bookPageUrl
        snip=context['code']=puzzle.codeSnippet
        context["pq"]=puzzle.puzzleQuestion
        context["puzzle"] = puzzle.puzzleDescription
        needip=context['needip']=puzzle.needsIP
        if needip:
            snip='If you are giving multiple input values, Seperate them using commas `,`'
            context['terminalval']=snip
    except Puzzle.DoesNotExist:
        # Handle the case where the puzzle with the given puzzleid is not found
        context["puzzleerror"] = "Puzzle not found for ID: {}".format(puzzleid)
        
    if request.method == "POST":
        # If the request method is POST, process the form submission
        
        # Retrieve language, code, and puzzleid from the POST data
        language = request.POST.get("language")
        code = request.POST.get("code")
        puzzleid = request.POST.get("pid")
        if needip:
            userinput=request.POST.get("user_input")
            # inp = [value.strip() for value in userinput.split(",")]
            inp = userinput.replace(",", "\n").strip()
        try:
            # Attempt to compile the code using the RapidAPI compiler service
            
            # Define API endpoint and payload
            url = "https://online-code-compiler.p.rapidapi.com/v1/"
            payload = {
                "language": language,
                "version": "latest",
                "code": code,
                "input": inp
            }
            headers = {
                "content-type": "application/json",
                "X-RapidAPI-Key": "#########",
                "X-RapidAPI-Host": "online-code-compiler.p.rapidapi.com"
            }
            
            # Send POST request to the compiler service
            response = requests.post(url, json=payload, headers=headers)
            result = response.json()
            output = result['output']
            
            # Update context with output and submitted code
            context['output'] = output
            context['code'] = code

        except Exception as e:
            # Handle any exceptions that occur during compilation
            context['compilererror'] = str(e)
        
        try:
            # Attempt to generate feedback using the OpenAI Chat API
            
            # Compose message for the AI chat, including code, puzzle question, and language
            sysmessage="You are going to act like a programming teacher talking to a student in a casual tone. Give feedback on their code. If the code is correct, then no additional feedback on good practices is to be given. VERY VERY IMPORTANTLY If the code is incorrect or the code doesn't STRICTLY match the requirements of the question or the output doesn't match the expected output from the question, then give the student feedback and instructions on how to fix the error and start the response with 'Uh-oh! Looks like there's a hiccup in your code.'"
            message = (
            "The student has submitted the following code:\n"
            f"{code}\n"
            "as the answer for the following question:"
            f"{puzzle.puzzleQuestion}\n"
            f"using {language}.\n\n"
            "and got the following output:\n"
            f"{output}\n"
            "Give your feedback (should be at most 5-6 lines) as a programming teacher."
            )
            if needip:
                sysmessage+="If input values are also there, comment on the correctness of input values in accordance to the question"
                message+=("n"
                f"The student gave {userinput} as input"      
                )
            # Create a list of messages for the chat
            messages = [{"role":"system","content":sysmessage},{"role": "user", "content": message}]
            # Send messages to the OpenAI Chat API and retrieve the response
            chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            reply = chat.choices[0].message.content
            # Update context with the generated feedback
            context["feedback"] = reply
        except Exception as f:
            # Handle any errors that occur during communication with the OpenAI API
            context['feedbackerror'] = str(f)
    # Render the home1.html template with the populated context
    return render(request, "code.html", context)

def index(request):
    return render(request, 'index.html')

def deleteprofile(request,id):
    delid=UserRegistration.objects.get(id=id)
    delid.delete()
    return render(request, 'adminhomepage.html')

def adminlogin(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        logobj=AdminRegistration.objects.filter(UserName=username,Password=password)
        if logobj:
            loginDetails=AdminRegistration.objects.get(UserName=username,Password=password)
            sessionID=loginDetails.id
            request.session['my_session']=sessionID
            return redirect('adminhomepage')
        else:
            error_message = "Invalid credentials! Please try again."
            return render(request, 'adminlogin.html', {'error_message': error_message})
    else:
        return render(request, 'adminlogin.html')

def adminprofile(request):
    userProfile=UserRegistration.objects.all()
    return render(request, 'adminprofile.html',{'data':userProfile})

def adminhomepage(request):
    return render(request, 'adminhomepage.html')

def adminfeedback(request):
    fb=Feedback.objects.all()
    return render(request, 'adminfeedback.html',{'fb':fb})

def about(request):
    return render(request, 'about.html')

def clevel(request):
    return render(request, 'clevel.html')

def plevel(request):
    return render(request, 'plevel.html')

def profile(request):
    if request.method == "POST":
        if 'submitUpdate' in request.POST:
            user_id = request.POST.get('id')
            username = request.POST.get('username')
            dob = request.POST.get('dob')
            gender = request.POST.get('gender')
            bio = request.POST.get('bio')

            # Get the current user's Profile
            profile = Profile.objects.get(Email=user_id)

            # Update the fields
            profile.UserName = username
            profile.DoB = dob
            profile.Gender = gender
            profile.Bio = bio
            profile.save()

            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        elif 'cancelUpdate' in request.POST:
            return redirect('profile')
    else:
        # Get the current user's Profile
        current_user = request.session.get('my_session')
        profile = Profile.objects.get(Email=current_user)

        # Data to pass to the template
        data = {
            'id': profile.id,
            'username': profile.UserName,
            'dob': profile.DoB,
            'gender': profile.Gender,
            'bio': profile.Bio,
        }

        return render(request, 'profile.html', data)

def profileupdate(request):
    current_user = request.session.get('my_session')
    profile = Profile.objects.get(Email=current_user)

        # Data to pass to the template
    data = {
            'id': current_user,
            'username': profile.UserName,
            'dob': profile.DoB,
            'gender': profile.Gender,
            'bio': profile.Bio,
        }
    print(data['dob'])
    return render(request, 'profileupdate.html',data)
   
def feedback(request):
    if(request.method=="POST"):
        name=request.POST.get("name")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        message=request.POST.get("message")
        Feedback(Name=name,Email=email,Phone=phone,Message=message).save()
        return redirect('homepage')
    else:
        return render(request, 'feedback.html')

def homepage(request):
    return render(request, 'homepage.html')

def course(request):
    return render(request, 'course.html')

def courses(request):
    return render(request, 'courses.html')

def bookpage(request,corp,level,page):
    if corp=='c':
        try:
            cr=CStory.objects.get(Level=level,Page=page)
            storyName='The C Cipher'
            urllang='c'
        except CStory.DoesNotExist:
            redirectpage=corp+"level"
            return redirect(redirectpage)
    elif corp=='p':
        try:
            cr=PyStory.objects.get(Level=level,Page=page)
            storyName='The Python Chronicles'
            urllang='python3'
        except PyStory.DoesNotExist:
            redirectpage=corp+"level"
            return redirect(redirectpage)
    title=cr.Title
    data=cr.Content
    hasPuzzle=cr.hasPuzzle
    pid=cr.PuzzleID
    prevp=page-1
    nextp=page+1
    p1=(page*2)-1
    p2=page*2
    return render(request, 'bookpage.html',{'title':title,'data':data,'p1':p1,'p2':p2,'story':storyName,
                                            'corp':corp,'level':level,'prev':prevp,'next':nextp,'hasPuzzle':hasPuzzle,'urllang':urllang,'pid':pid})

def reglog(request):
    if(request.method=="POST"):
        if 'signupFormSubmit' in request.POST:
            email=request.POST.get("email")
            password=request.POST.get("password")
            regobj=UserRegistration.objects.filter(Email=email)
            if regobj:
                error_message = "Email already in use! Please try another or login."
                return render(request, 'reglog.html', {'error_message': error_message})
            else:
                UserRegistration(Email=email,Password=password).save()
                return redirect('reglog')
        elif 'loginFormSubmit' in request.POST:
            email=request.POST.get("email")
            password=request.POST.get("password")
            logobj=UserRegistration.objects.filter(Email=email,Password=password)
            if logobj:
                loginDetails=UserRegistration.objects.get(Email=email,Password=password)
                sessionID=loginDetails.Email
                request.session['my_session']=sessionID
                return redirect('homepage')
            else:
                error_message = "Invalid credentials! Please try again."
                return render(request, 'reglog.html', {'error_message': error_message})
    else:
        return render(request,'reglog.html')