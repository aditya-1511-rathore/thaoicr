from django.shortcuts import render, redirect
from .forms import OCRForm
from .models import OCRResult
# import pytesseract
# from PIL import Image
# from io import BytesIO
from django.http import JsonResponse
from .forms import OCRForm
from .process_image import process_image
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
def home(request):
    if request.method == "POST":
        form = OCRForm(request.POST, request.FILES)
        if form.is_valid():
            # get the image from the form
            image = form.cleaned_data["image"]

            # save the image in the corrosponding folder!
            fs = FileSystemStorage(location='ocr_images/')
            filename = fs.save(image.name, image)
            
            # send the file name into the function to process and extract the data from the image\
            binary_conversion = False
            if "binary" in request.POST.keys():
                binary_conversion = True
            result, raw = process_image(filename, binary_conversion)
            if result == "Error":
                return HttpResponse("Error occured while performing OCR on id card!")
            id = result["id"]
            
            # save the result into the database
            if OCRResult.objects.filter(id_number = id).count() == 0:
                data = OCRResult.objects.create(
                    image = image, 
                    text = result,
                    id_number = result["id"],
                    name = result["name"],
                    last_name = result["last_name"],
                    date_of_birth = result["date-of-birth"],
                    date_of_issue = result["date-of-issue"],
                    date_of_expiry = result["date-of-expiry"],
                    success = result["status"]
                    )
                return render(request,"item.html",context={"data":data, "new":True})
            else:
                return redirect(f"/previous?id={OCRResult.objects.get(id_number = id).id}&exist=True")
    return render(request, "home.html", {"form":OCRForm()})

# function to view all the previous scans
def previous(request):
    # if id is in the get request, that means the user requested to see the detailed view of a id number
    if "id" in request.GET.keys():
        if request.method == "POST":
            # to delete the requested ID
            if request.POST.get("type") == "delete":
                OCRResult.objects.get(id = request.GET["id"]).delete()
                return redirect("/previous")
            
            # to update the requested id
            else:
                ocr_val = OCRResult.objects.get(id = request.GET["id"])
                ocr_val.id_number = request.POST["id_number"]
                ocr_val.name = request.POST["name"]
                ocr_val.last_name = request.POST["lname"]
                ocr_val.date_of_birth = request.POST["dob"]
                ocr_val.date_of_expiry = request.POST["doe"]
                ocr_val.date_of_issue = request.POST["doi"]
                ocr_val.success = True
                ocr_val.save()
                id_red = request.GET["id"]
                return redirect(f"/previous?id={id_red}")
        if "exist" in request.GET.keys():
            return render(request, "item.html", context={"data":OCRResult.objects.get(id = request.GET["id"]),"exist":True})

        return render(request, "item.html", context={"data":OCRResult.objects.get(id = request.GET["id"])})
    return render(request,"previous.html", context = {"data":OCRResult.objects.all()})
