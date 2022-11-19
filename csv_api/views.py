from django.contrib import messages
from .forms import UploadFileForm
import logging
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt 
def upload_csv(request):
    if "GET" == request.method:
        # return HttpResponse("hello")
        return HttpResponse("failed")
    try:
        form = UploadFileForm(request.POST, request.FILES)
        print(request.FILES)
        for field in form:
            print("Field Error:", field.name,  field.errors)
        if form.is_valid():
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request,'File is not CSV type')
                return Http404()
            #if file is too large, return
            if csv_file.multiple_chunks():
                messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
                return Http404()

            file_data = csv_file.read().decode("utf-8")		

            lines = file_data.split("\n")
            print(lines)
        return HttpResponse("success")
    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))

        return HttpResponse("failed")