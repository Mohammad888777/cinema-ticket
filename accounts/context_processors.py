from .forms import SignupForm


def signUpFormControl(request):

    return {
        "form":SignupForm(),

    }

# "context_processors"