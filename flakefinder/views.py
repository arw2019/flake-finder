from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import render
from django.utils import timezone

from .forms import UploadFileForm

from .models import Chip

from .thresholding import Thresholder


def index(request):
    return render(request, "flakefinder/index.html")


@login_required
def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        try:
            image_file = request.FILES["image"]
            thresh = Thresholder(image_file)

            if not thresh.areas:
                msg = "There are no usable flakes in this image."
            else:
                labelled_image_name = (
                    image_file.name[:-4] + "_labelled" + image_file.name[-4:]
                )
                labelled_image = SimpleUploadedFile(
                    labelled_image_name, thresh._image_with_labels()
                )

                new_chip = Chip(
                    name=request.FILES["image"],
                    date_created=timezone.now(),
                    original_image=image_file,
                    labelled_image=labelled_image,
                    num_flakes=len(thresh.areas),
                )
                new_chip.save()

                msg = f" {len(thresh.regions)} usable flakes were found."

        except Exception as e:
            msg = "File could not be uploaded."
            # raise e

    else:
        msg = "Please upload a file."

    context = {'message': msg}

    return render(request, "flakefinder/upload.html", context)


@login_required
def search_chips(request):
    chip_selection = Chip.objects.order_by("-date_created")[:5]

    chip_list = [
        (chip.name, chip.date_created, chip.num_flakes)
        for chip in chip_selection
    ]

    context = {"chip_list": chip_list}

    return render(request, "flakefinder/search_chips.html", context)
