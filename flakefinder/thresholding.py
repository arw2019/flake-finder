from io import BytesIO
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import skimage.io
from skimage.filters import threshold_otsu
from skimage.morphology import closing, square
from skimage.measure import label, regionprops

__all__ = ["Thresholder"]


class Thresholder:
    def __init__(self, fname=None):
        self._fname = fname
        self._original = None
        self._image = None
        self._regions = None

    def __str__(self):
        return self._fname

    @property
    def regions(self):
        if self._regions is None:
            self._find_flakes()
        return self._regions

    @property
    def fname(self):
        return self._fname

    @fname.setter
    def fname(self, fname):
        self._fname = fname

    @property
    def regions(self, upper_limit=float("inf"), lower_limit=5000):
        if self._regions is None:
            self._find_flakes()
        self._regions = [
            region
            for region in self._regions
            if lower_limit < region.area < upper_limit
        ]

    @property
    def areas(self, upper_limit=float("inf"), lower_limit=5000):
        return [region.area for region in self.regions]

    def _find_flakes(self):
        self._load_image()
        self._remove_white()
        self._select_channel("G")
        self._do_thresholding()

    def _do_thresholding(self):
        thresh = threshold_otsu(self._image)
        bw = closing(self._image > thresh, square(3))
        self._image_labelled = label(bw, background=0)
        self._regions = regionprops(self._image_labelled)

    def _load_image(self):
        try:
            self._image = skimage.io.imread(self._fname)
        except Exception as e:
            raise ValueError("Cannot load image") from e

    def _remove_white(self, arrow_threshold=250) -> None:
        def func(x):
            return x if x < arrow_threshold else 0

        self._image = np.vectorize(func)(self._image)

    def _select_channel(self, choice: str) -> None:
        # TO DO: implement this for len(choice)!=1
        if len(choice) != 1:
            raise NotImplementedError
        selection = "RBG".find(choice)
        self._image = self._image[:, :, selection]

    def _image_with_labels(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(self._image)

        for region in self.regions:
            minr, minc, maxr, maxc = region.bbox
            rect = mpatches.Rectangle(
                (minc, minr),
                maxc - minc,
                maxr - minr,
                fill=False,
                edgecolor="red",
                linewidth=2,
            )
            ax.add_patch(rect)

        fig_data = BytesIO()
        fig.savefig(fig_data, format="jpg")
        return fig_data.getvalue()
