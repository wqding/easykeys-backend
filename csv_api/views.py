from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render
import logging
from django.http import HttpResponse, Http404, HttpResponseRedirect

# Create your views here.
def upload_csv(request):
    if "GET" == request.method:
        # return HttpResponse("hello")
        return Http404()
    try:
        print(request)
        print(request.FILES)
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("csv_api:upload_csv"))
        #if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("csv_api:upload_csv"))

        file_data = csv_file.read().decode("utf-8")		

        lines = file_data.split("\n")
        print(lines)
    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))

    return HttpResponseRedirect(reverse("csv_api:upload_csv"))