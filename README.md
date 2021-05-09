# MTF and Linearity Analysis

MTF and image linearity functions are implemented in [MTF.py](MTF.py) and [ImgLinearity.py](ImgLinearity.py). The MTF class takes a cropped image containing only a Siemens star chart, and the ImgLinearity class takes an X-Rite ColorChecker chart and utilizes the colorimetric data found [here](https://xritephoto.com/ph_product_overview.aspx?ID=820&Action=support&SupportID=5159) to create linearity plots for R, G, and B channels in an image.

The [utilities](utilities) folder contains some custom utilities I've created to facilitate sharpness, resolution, and linearity metrics in various projects.

The `MTF_*.ipnyb` files in [sample_analysis](sample_analysis) contain sample analyses I have done using both the `MTF` and `ImgLinearity` classes.

Sample [.png](star_chart_sine.png) and [.pdf](star_chart_sine.pdf) star charts are also provided.

## Resources
* Useful resource for finding pixels to crop from: https://yangcha.github.io/iview/iview.html
* MTF paper: https://arxiv.org/pdf/1805.01872.pdf
* [Link](http://www.bealecorner.org/red/test-patterns/star-chart-sine144-720dpi.png) to high resolution test patterns
* Star chart links:
    * [Article](https://harvestimaging.com/blog/?p=1294) on how to measure MTF with a star chart.
    * German [paper](https://www.image-engineering.de/content/library/diploma_thesis/anke_neumann_aufloesungsmessung.pdf), English [equivalent](https://image-engineering.de/content/library/conference_papers/2007_03_12/EI_2007_6502_21.PDF)
    * https://www.imatest.com/docs/starchart/
    * Fatima Kahil's [Github page](https://fakahil.github.io/solo/how-to-use-the-siemens-star-calibration-target-to-obtain-the-mtf-of-an-optical-system/index.html)
* [Article](https://lenspire.zeiss.com/photo/app/uploads/2018/04/CLN_MTF_Kurven_2_en.pdf) by Zeiss
    
