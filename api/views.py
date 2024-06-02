from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader

from .inference.summary import Summarizer
from .Preprocessor import Preprocessor
from django.views.decorators.csrf import csrf_exempt

summarizer = Summarizer()


@csrf_exempt
def index(request):
    processor = Preprocessor()
    content = processor.clean(request.POST['content'])
    print(content)
    if len(content) <= 10 or len(content) >= 20000:
        return JsonResponse({"summary": "Can't summarize this!"})
    text = summarizer.summarize(content)
    return JsonResponse({"summary": processor.formater(text)})


def test(request):
    text = summarizer.summarize(summarizer.text)
    return HttpResponse(Preprocessor().formater(text))


@csrf_exempt
def directSummary(request):
    processor = Preprocessor()
    template = loader.get_template('contextForm.html')
    content = processor.clean(request.POST['content'])
    if len(content) <= 10 or len(content) >= 20000:
        return HttpResponse(template.render({'userInput': content, 'summary': "Can't summarize this!"}, request))
    print("Direct: ", content)
    text = summarizer.summarize(content)
    return HttpResponse(template.render({'userInput': content, 'summary': processor.formater(text)}, request))


def directForm(request):
    template = loader.get_template('contextForm.html')
    return HttpResponse(template.render())
