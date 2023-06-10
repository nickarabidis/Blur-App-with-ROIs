import numpy as np
import tkinter as tk
import cv2
import sys
import PIL
import os
import sys
from tkinter import ttk
from tkinter import (
    Frame,
    Label,
    Canvas,
    Button,
    OptionMenu,
    StringVar,
    Toplevel,
    Entry,
    messagebox,
    PhotoImage,
)
from PIL import Image, ImageTk
from tkinter import filedialog as tkFileDialog


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


Blur_options = [
    "Averaging Blurring",
    "Gaussian Blurring",
    "Median Blurring",
    "Bilateral Filtering",
]
ROIs_options = ["Rectangle ROIs", "Circle ROIs"]
root = tk.Tk()
root.title("Blur App")
root.geometry("1050x650")
root.resizable(False, False)
root.config(bg="#343541")
ROIs = []
ROIs2 = []
brush_size = 10

default_blur = StringVar(root)
default_blur.set("Averaging Blurring")
default_roi = StringVar(root)
default_roi.set("Rectangle ROIs")

IconPhoto = PhotoImage(file=resource_path("images/logo.png"))
root.iconphoto(True, IconPhoto)

# blur defaults
Kernel_boxX = tk.StringVar()
Kernel_boxX.set("5")

Kernel_boxY = tk.StringVar()
Kernel_boxY.set("5")

Gauss_KernelX = tk.StringVar()
Gauss_KernelX.set("5")

Gauss_KernelY = tk.StringVar()
Gauss_KernelY.set("5")

Gauss_SigX = tk.StringVar()
Gauss_SigX.set("0")

Gauss_SigY = tk.StringVar()
Gauss_SigY.set("0")

Median_KernelX = tk.StringVar()
Median_KernelX.set("5")

Bi_Nei = tk.StringVar()
Bi_Nei.set("9")

Bi_Color = tk.StringVar()
Bi_Color.set("75")

Bi_Space = tk.StringVar()
Bi_Space.set("75")

# Create a sharpening kernel
Sharpen_Kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])

# Create a Deblur kernel
Deblur_Kernel_StrengthDenoising = tk.StringVar()
Deblur_Kernel_StrengthDenoising.set("10")

Deblur_Kernel_StrengthColor = tk.StringVar()
Deblur_Kernel_StrengthColor.set("7")

Deblur_Kernel_WindowSize = tk.StringVar()
Deblur_Kernel_WindowSize.set("21")

# Frames for left and right side
left_frame = Frame(root, width=150, height=600, bg="#444654")
left_frame.grid(row=0, column=0, padx=10, pady=15, sticky="nsew")

right_frame = Frame(root, width=850, height=600, bg="#444654")
right_frame.grid(row=0, column=1, padx=10, pady=15, sticky="nsew")

# Left frame

tools_Label = Label(
    left_frame,
    text="Tools:",
    font=(14),
    relief="ridge",
    bg="#343541",
    fg="white",
)
tools_Label.grid(row=1, column=0, padx=5, pady=10, ipadx=5, ipady=5)

tools_sidebar = Frame(left_frame, width=100, height=600, bg="#343541")
tools_sidebar.grid(row=2, column=0, padx=10, pady=10)


filters_Label = Label(
    left_frame,
    text="Filters:",
    font=(14),
    relief="ridge",
    bg="#343541",
    fg="white",
)
filters_Label.grid(row=3, column=0, padx=5, pady=10, ipadx=5, ipady=5)

filters_sidebar = Frame(left_frame, width=100, height=600, bg="#343541")
filters_sidebar.grid(row=4, column=0, padx=10, pady=10)


# Right frame
start_image = Image.open(resource_path("images/start_image.png"))
I = cv2.imread(resource_path("images/start_image.png"))
I_reset = I.copy()
save = cv2.imread(resource_path("images/start_image.png"))
resized_start_img = start_image.resize((850, 600))
start_img = ImageTk.PhotoImage(resized_start_img)

canvas = Canvas(right_frame, width=850, height=600, bg="#444654")
container = canvas.create_image(0, 0, image=start_img, anchor=tk.NW)
canvas.grid(row=0, column=0, padx=5, pady=5)


def import_file():
    global I, I_reset, save, ROIs, ROIs2

    filetypes = [("PNG Files", "*.png"), ("JPEG Files", "*.jpg")]

    path = tkFileDialog.askopenfilename(
        title="Select an Image File", filetypes=filetypes
    )

    if len(path) != 0:
        I = cv2.imread(path)
        I_reset = I.copy()
        save = cv2.imread(path)
        origin_image = Image.open(path)

        resized_img = origin_image.resize((850, 600))
        img = ImageTk.PhotoImage(resized_img)
        canvas.itemconfig(container, image=img)
        canvas.imgref = img
        ROIs.clear()
        ROIs2.clear()


def export_window():
    global Save_Entry, Svariable, X_Entry, Y_Entry, SaveWin

    SaveWin = Toplevel(root)
    SaveWin.resizable(False, False)
    SAoptions = [".png", ".jpg"]
    Svariable = StringVar(SaveWin)
    Svariable.set(".png")

    SaveFrame = Frame(SaveWin, width=180, height=185, bg="#343541")
    SaveFrame.grid(row=0, column=0)

    Save_window = Frame(SaveFrame, width=50, height=50, bg="#343541")
    Save_window.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5)

    Save_L = Label(
        Save_window, text="Saving Options", relief="ridge", bg="#444654", fg="white"
    ).grid(row=0, column=0, padx=5, pady=3, ipadx=10)
    Save_labe = Label(
        Save_window, text="File Name:", relief="ridge", bg="#444654", fg="white"
    ).grid(row=1, column=0, ipadx=10)
    Save_Entry = Entry(Save_window)
    Save_Entry.insert(0, "Blurred Image")
    Save_Entry.grid(row=1, column=1, padx=5, pady=3, ipadx=10)

    Save_DropM = OptionMenu(Save_window, Svariable, *SAoptions).grid(
        row=1, column=2, sticky="w", padx=5, pady=3, ipadx=10
    )

    Save_Button = Button(
        Save_window,
        text="Save",
        relief="ridge",
        bg="#444654",
        fg="white",
        command=lambda: export_file(1),
    ).grid(row=1, column=3, ipadx=10, sticky="news")
    Save_As_Button = Button(
        Save_window,
        text="Save As",
        relief="ridge",
        bg="#444654",
        fg="white",
        command=lambda: export_file(2),
    ).grid(row=1, column=4, ipadx=10, sticky="news")
    Ysave = Label(
        Save_window, text="Image Height:", relief="ridge", bg="#444654", fg="white"
    ).grid(row=2, column=0, padx=5, pady=3, ipadx=10)
    Xsave = Label(
        Save_window, text="Image Length:", relief="ridge", bg="#444654", fg="white"
    ).grid(row=3, column=0, padx=5, pady=3, ipadx=10)
    X_Entry = Entry(Save_window, width=3)
    X_Entry.grid(row=2, column=1, sticky="w", padx=5, pady=3, ipadx=10)
    Y_Entry = Entry(Save_window, width=3)
    Y_Entry.grid(row=3, column=1, sticky="w", padx=5, pady=3, ipadx=10)


def export_file(options):
    global Save_Entry, save, Svariable, Y_Entry, X_Entry
    Filename = []

    if len(Save_Entry.get()):
        if options == 2:
            Save_Path = tkFileDialog.askdirectory()
            if len(Save_Path) != 0:
                if Y_Entry.get() != "" and X_Entry.get() != "":
                    if Y_Entry.get().isnumeric() and X_Entry.get().isnumeric():
                        if int(Y_Entry.get()) > 0 and int(X_Entry.get()) > 0:
                            save = cv2.resize(
                                save, (int(X_Entry.get()), int(Y_Entry.get()))
                            )
                os.chdir(Save_Path)
                Filename.append(Save_Entry.get())
                Filename.append(Svariable.get()[1:4])
                cv2.imwrite(".".join(Filename), save)
                SaveWin.destroy()
        else:
            Filename.append(Save_Entry.get())
            Filename.append(Svariable.get()[1:4])
            if Y_Entry.get() != "" and X_Entry.get() != "":
                if Y_Entry.get().isnumeric() and X_Entry.get().isnumeric():
                    if int(Y_Entry.get()) > 0 and int(X_Entry.get()) > 0:
                        save = cv2.resize(
                            save, (int(X_Entry.get()), int(Y_Entry.get()))
                        )
            cv2.imwrite(".".join(Filename), save)
            SaveWin.destroy()


def start_crop():
    global I, I_reset, ROIs2, center, choice
    roiPicker()
    canvasRemake(I)
    # choice = default_roi.get()
    # if choice == "Rectangle ROIs":
    #     roiPicker1()
    # else:
    #     cv2.imshow("Select ROIs", I)
    #     cv2.setMouseCallback("Select ROIs", roiPicker2)


def roiPicker():
    global I, I_reset, ROIs, center, ROIs2

    choice = default_roi.get()
    if choice == "Rectangle ROIs":
        # select ROIs function
        # keep getting ROIs until pressing 'q'
        while True:
            # get ROI cv2.selectROI(window_name, image_matrix, selecting_start_point)

            cv2.namedWindow("Select ROIs", 2)
            box = cv2.selectROI("Select ROIs", I, False, False)

            # add selected box to box list
            ROIs.append(box)

            # draw a rectangle on selected ROI
            I = cv2.rectangle(
                I, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), (255, 0, 0), 2
            )
            I_reset = I.copy()
            print(
                "ROI is saved, press q to stop capturing, press any other key to select other ROI"
            )
            # if 'q' is pressed then break
            key = cv2.waitKey(0)
            if key & 0xFF == ord("q"):
                break

    elif choice == "Circle ROIs":
        while True:
            # get ROI cv2.selectROI(window_name, image_matrix, selecting_start_point)
            box2 = cv2.selectROI("Select ROIs", I, fromCenter=False)

            # calculate the center and radius of the circle based on the selected box
            center = (int(box2[0] + box2[2] / 2), int(box2[1] + box2[3] / 2))
            radius = int(max(box2[2], box2[3]) / 2)

            # add selected circle parameters to the ROIs list
            ROIs2.append((center, radius))

            # draw a circle on the selected ROI
            I = cv2.circle(I, center, radius, (255, 0, 0), 2)

            print(
                "ROI is saved, press q to stop capturing, press any other key to select other ROI"
            )
            # if 'q' is pressed then break
            key = cv2.waitKey(0)
            if key & 0xFF == ord("q"):
                break

    canvasRemake(I)


# def roiPicker2(event, x, y, flags, param):
#     global I, I_reset, ROIs, center, ROIs2

#     choice = default_roi.get()
#     if choice == "Circle ROIs":
#         if event == cv2.EVENT_LBUTTONDOWN:
#             # Calculate the radius as the distance from the center to the clicked point
#             radius = int(((x - center[0]) ** 2 + (y - center[1]) ** 2) ** 0.5)

#             # Add selected circle parameters to the ROIs list
#             ROIs2.append((center, radius))

#             # Draw a circle on the selected ROI
#             I = cv2.circle(I, center, radius, (255, 0, 0), 2)
#             I = image
#             I_reset = I.copy()
#             cv2.imshow("Pick places to blur", image)

#             print(
#                 "ROI is saved, press q to stop capturing, press any other key to select another ROI"
#             )

#         elif event == cv2.EVENT_RBUTTONDOWN:
#             # Reset the center point if right-clicked
#             center = (x, y)

#         canvasRemake(I)


def canvasRemake(I1):
    I1 = cv2.cvtColor(I1, cv2.COLOR_BGR2RGB)
    N = cv2.resize(I1, (850, 600))
    N = ImageTk.PhotoImage(image=Image.fromarray(N))
    canvas.itemconfig(container, image=N)
    canvas.imgref = N


def blur():
    global I, I_reset, ROIs, ROIs2, center, EnNeibor, EnSigCol, EnSigSpa, EnKerX, EnKerY, EnKerX1, EnKerY1, EnSigmX, EnSigmY, EnKerX2
    choice = default_blur.get()
    choice2 = default_roi.get()
    if choice2 == "Rectangle ROIs":
        if choice == "Averaging Blurring":
            for box in ROIs:
                # unpack each box
                x, y, w, h = [d for d in box]

                # crop the image due to the current box
                sub = I[y : y + h, x : x + w]
                sub2 = save[y : y + h, x : x + w]
                # apply Blur on cropped area
                blur = cv2.blur(sub, (int(Kernel_boxX.get()), int(Kernel_boxY.get())))
                blur2 = cv2.blur(sub2, (int(Kernel_boxX.get()), int(Kernel_boxY.get())))

                # paste blurred image on the original image
                I[y : y + h, x : x + w] = blur
                save[y : y + h, x : x + w] = blur2

                canvasRemake(I)
        elif choice == "Gaussian Blurring":
            for box in ROIs:
                # unpack each box
                x, y, w, h = [d for d in box]

                # crop the image due to the current box
                sub = I[y : y + h, x : x + w]
                sub2 = save[y : y + h, x : x + w]

                # apply GaussianBlur on cropped area

                blur = cv2.GaussianBlur(
                    sub,
                    (int(Gauss_KernelX.get()), int(Gauss_KernelY.get())),
                    int(Gauss_SigX.get()),
                    int(Gauss_SigY.get()),
                )
                blur2 = cv2.GaussianBlur(
                    sub2,
                    (int(Gauss_KernelX.get()), int(Gauss_KernelY.get())),
                    int(Gauss_SigX.get()),
                    int(Gauss_SigY.get()),
                )

                # paste blurred image on the original image
                I[y : y + h, x : x + w] = blur
                save[y : y + h, x : x + w] = blur2

                canvasRemake(I)
        elif choice == "Median Blurring":
            for box in ROIs:
                # unpack each box
                x, y, w, h = [d for d in box]

                # crop the image due to the current box
                sub = I[y : y + h, x : x + w]
                sub2 = save[y : y + h, x : x + w]

                # apply medianBlur on cropped area

                blur = cv2.medianBlur(sub, int(Median_KernelX.get()))
                blur2 = cv2.medianBlur(sub2, int(Median_KernelX.get()))

                # paste blurred image on the original image
                I[y : y + h, x : x + w] = blur
                save[y : y + h, x : x + w] = blur2

                canvasRemake(I)
        elif choice == "Bilateral Filtering":
            for box in ROIs:
                # unpack each box
                x, y, w, h = [d for d in box]

                # crop the image due to the current box
                sub = I[y : y + h, x : x + w]
                sub2 = save[y : y + h, x : x + w]

                # apply bileteralBlur on cropped area

                blur = cv2.bilateralFilter(
                    sub, int(Bi_Nei.get()), int(Bi_Color.get()), int(Bi_Space.get())
                )
                blur2 = cv2.bilateralFilter(
                    sub2, int(Bi_Nei.get()), int(Bi_Color.get()), int(Bi_Space.get())
                )

                # paste blurred image on the original image
                I[y : y + h, x : x + w] = blur
                save[y : y + h, x : x + w] = blur2

                canvasRemake(I)
    elif choice2 == "Circle ROIs":
        if choice == "Averaging Blurring":
            for circle in ROIs2:
                # unpack the circle parameters
                center, radius = circle
                print(circle)

                # calculate the bounding box for the circle
                x, y = int(center[0] - radius), int(center[1] - radius)
                w, h = int(2 * radius), int(2 * radius)

                # crop the image due to the current circle
                sub3 = I[y : y + h, x : x + w]
                sub4 = save[y : y + h, x : x + w]

                # apply Blur on cropped area
                blur = cv2.blur(sub3, (int(Kernel_boxX.get()), int(Kernel_boxY.get())))
                blur2 = cv2.blur(sub4, (int(Kernel_boxX.get()), int(Kernel_boxY.get())))

                # create a mask with the same size as the sub-image, filled with zeros
                mask = np.zeros_like(sub3)
                mask2 = np.zeros_like(sub4)

                # create a circle on the mask with the same size as the sub-image
                cv2.circle(mask, (radius, radius), radius, (255, 255, 255), -1)
                cv2.circle(mask2, (radius, radius), radius, (255, 255, 255), -1)

                # apply the mask to the blurred image
                blurred_roi = cv2.bitwise_and(blur, mask)
                blurred_roi2 = cv2.bitwise_and(blur2, mask2)

                # paste blurred ROI on the original image
                I[y : y + h, x : x + w] = blurred_roi
                save[y : y + h, x : x + w] = blurred_roi2

                canvasRemake(I)
        elif choice2 == "Gaussian Blurring":
            for circle in ROIs2:
                # unpack the circle parameters
                center, radius = circle

                # calculate the bounding box for the circle
                x, y = int(center[0] - radius), int(center[1] - radius)
                w, h = int(2 * radius), int(2 * radius)

                # crop the image due to the current circle
                sub3 = I[y : y + h, x : x + w]
                sub4 = save[y : y + h, x : x + w]

                # apply GaussianBlur on cropped area
                blur = cv2.GaussianBlur(
                    sub3,
                    (int(Gauss_KernelX.get()), int(Gauss_KernelY.get())),
                    int(Gauss_SigX.get()),
                    int(Gauss_SigY.get()),
                )
                blur2 = cv2.GaussianBlur(
                    sub4,
                    (int(Gauss_KernelX.get()), int(Gauss_KernelY.get())),
                    int(Gauss_SigX.get()),
                    int(Gauss_SigY.get()),
                )

                # create a mask with the same size as the sub-image, filled with zeros
                mask = np.zeros_like(sub3)
                mask2 = np.zeros_like(sub4)

                # create a circle on the mask with the same size as the sub-image
                cv2.circle(mask, (radius, radius), radius, (255, 255, 255), -1)
                cv2.circle(mask2, (radius, radius), radius, (255, 255, 255), -1)

                # apply the mask to the blurred image
                blurred_roi = cv2.bitwise_and(blur, mask)
                blurred_roi2 = cv2.bitwise_and(blur2, mask2)

                # paste blurred ROI on the original image
                I[y : y + h, x : x + w] = blurred_roi
                save[y : y + h, x : x + w] = blurred_roi2

                canvasRemake(I)
        elif choice2 == "Median Blurring":
            for circle in ROIs2:
                # unpack the circle parameters
                center, radius = circle

                # calculate the bounding box for the circle
                x, y = int(center[0] - radius), int(center[1] - radius)
                w, h = int(2 * radius), int(2 * radius)

                # crop the image due to the current circle
                sub3 = I[y : y + h, x : x + w]
                sub4 = save[y : y + h, x : x + w]

                # apply medianBlur on cropped area
                blur = cv2.medianBlur(sub3, int(Median_KernelX.get()))
                blur2 = cv2.medianBlur(sub4, int(Median_KernelX.get()))

                # create a mask with the same size as the sub-image, filled with zeros
                mask = np.zeros_like(sub3)
                mask2 = np.zeros_like(sub4)

                # create a circle on the mask with the same size as the sub-image
                cv2.circle(mask, (radius, radius), radius, (255, 255, 255), -1)
                cv2.circle(mask2, (radius, radius), radius, (255, 255, 255), -1)

                # apply the mask to the blurred image
                blurred_roi = cv2.bitwise_and(blur, mask)
                blurred_roi2 = cv2.bitwise_and(blur2, mask2)

                # paste blurred ROI on the original image
                I[y : y + h, x : x + w] = blurred_roi
                save[y : y + h, x : x + w] = blurred_roi2

                canvasRemake(I)
        elif choice2 == "Bilateral Filtering":
            for circle in ROIs2:
                # unpack the circle parameters
                center, radius = circle

                # calculate the bounding box for the circle
                x, y = int(center[0] - radius), int(center[1] - radius)
                w, h = int(2 * radius), int(2 * radius)

                # crop the image due to the current circle
                sub3 = I[y : y + h, x : x + w]
                sub4 = save[y : y + h, x : x + w]

                # apply bileteralBlur on cropped area

                blur = cv2.bilateralFilter(
                    sub3, int(Bi_Nei.get()), int(Bi_Color.get()), int(Bi_Space.get())
                )
                blur2 = cv2.bilateralFilter(
                    sub4, int(Bi_Nei.get()), int(Bi_Color.get()), int(Bi_Space.get())
                )

                # create a mask with the same size as the sub-image, filled with zeros
                mask = np.zeros_like(sub3)
                mask2 = np.zeros_like(sub4)

                # create a circle on the mask with the same size as the sub-image
                cv2.circle(mask, (radius, radius), radius, (255, 255, 255), -1)
                cv2.circle(mask2, (radius, radius), radius, (255, 255, 255), -1)

                # apply the mask to the blurred image
                blurred_roi = cv2.bitwise_and(blur, mask)
                blurred_roi2 = cv2.bitwise_and(blur2, mask2)

                # paste blurred ROI on the original image
                I[y : y + h, x : x + w] = blurred_roi
                save[y : y + h, x : x + w] = blurred_roi2

                canvasRemake(I)


###########################################


def deblur():
    global I, ROIs, ROIs2, center, EnNeibor, EnSigCol, EnSigSpa, EnKerX, EnKerY, EnKerX1, EnKerY1, EnSigmX, EnSigmY, EnKerX2, DeStrengthDen, DeStrengthCol, DeWindowSi
    choice = default_blur.get()
    choice2 = default_roi.get()
    if choice2 == "Rectangle ROIs":
        if choice == "Averaging Blurring":
            for box in ROIs:
                # unpack each box
                x, y, w, h = [d for d in box]

                # crop the image due to the current box
                sub = I[y : y + h, x : x + w]
                sub2 = save[y : y + h, x : x + w]
                # apply DeBlur on cropped area
                wiener_img = cv2.fastNlMeansDenoising(
                    sub,
                    None,
                    int(Deblur_Kernel_StrengthDenoising.get()),
                    int(Deblur_Kernel_StrengthColor.get()),
                    int(Deblur_Kernel_WindowSize.get()),
                )
                wiener_img2 = cv2.fastNlMeansDenoising(
                    sub2,
                    None,
                    int(Deblur_Kernel_StrengthDenoising.get()),
                    int(Deblur_Kernel_StrengthColor.get()),
                    int(Deblur_Kernel_WindowSize.get()),
                )

                # paste blurred image on the original image
                I[y : y + h, x : x + w] = wiener_img
                save[y : y + h, x : x + w] = wiener_img2

                canvasRemake(I)
        elif choice == "Gaussian Blurring":
            for box in ROIs:
                # unpack each box
                x, y, w, h = [d for d in box]

                # crop the image due to the current box
                sub = I[y : y + h, x : x + w]
                sub2 = save[y : y + h, x : x + w]

                # apply Deblur on cropped area

                wiener_img = cv2.fastNlMeansDenoising(
                    sub,
                    None,
                    int(Deblur_Kernel_StrengthDenoising.get()),
                    int(Deblur_Kernel_StrengthColor.get()),
                    int(Deblur_Kernel_WindowSize.get()),
                )
                wiener_img2 = cv2.fastNlMeansDenoising(
                    sub2,
                    None,
                    int(Deblur_Kernel_StrengthDenoising.get()),
                    int(Deblur_Kernel_StrengthColor.get()),
                    int(Deblur_Kernel_WindowSize.get()),
                )

                # paste blurred image on the original image
                I[y : y + h, x : x + w] = wiener_img
                save[y : y + h, x : x + w] = wiener_img2

                canvasRemake(I)
        elif choice == "Median Blurring":
            for box in ROIs:
                # unpack each box
                x, y, w, h = [d for d in box]

                # crop the image due to the current box
                sub = I[y : y + h, x : x + w]
                sub2 = save[y : y + h, x : x + w]

                # apply medianBlur on cropped area

                blur = cv2.medianBlur(sub, int(Median_KernelX.get()))
                blur2 = cv2.medianBlur(sub2, int(Median_KernelX.get()))

                # paste blurred image on the original image
                I[y : y + h, x : x + w] = blur
                save[y : y + h, x : x + w] = blur2

                canvasRemake(I)
        elif choice == "Bilateral Filtering":
            for box in ROIs:
                # unpack each box
                x, y, w, h = [d for d in box]

                # crop the image due to the current box
                sub = I[y : y + h, x : x + w]
                sub2 = save[y : y + h, x : x + w]

                # apply Deblur on cropped area

                wiener_img = cv2.fastNlMeansDenoising(
                    sub,
                    None,
                    int(Deblur_Kernel_StrengthDenoising.get()),
                    int(Deblur_Kernel_StrengthColor.get()),
                    int(Deblur_Kernel_WindowSize.get()),
                )
                wiener_img2 = cv2.fastNlMeansDenoising(
                    sub2,
                    None,
                    int(Deblur_Kernel_StrengthDenoising.get()),
                    int(Deblur_Kernel_StrengthColor.get()),
                    int(Deblur_Kernel_WindowSize.get()),
                )

                # paste blurred image on the original image
                I[y : y + h, x : x + w] = wiener_img
                save[y : y + h, x : x + w] = wiener_img2

                canvasRemake(I)
    elif choice2 == "Circle ROIs":
        if choice == "Averaging Blurring":
            for circle in ROIs2:
                # unpack the circle parameters
                center, radius = circle

                # calculate the bounding box for the circle
                x, y = int(center[0] - radius), int(center[1] - radius)
                w, h = int(2 * radius), int(2 * radius)

                # crop the image due to the current circle
                sub3 = I[y : y + h, x : x + w]
                sub4 = save[y : y + h, x : x + w]

                # apply DeBlur on cropped area
                wiener_img = cv2.fastNlMeansDenoising(
                    sub3,
                    None,
                    int(Deblur_Kernel_StrengthDenoising.get()),
                    int(Deblur_Kernel_StrengthColor.get()),
                    int(Deblur_Kernel_WindowSize.get()),
                )
                wiener_img2 = cv2.fastNlMeansDenoising(
                    sub4,
                    None,
                    int(Deblur_Kernel_StrengthDenoising.get()),
                    int(Deblur_Kernel_StrengthColor.get()),
                    int(Deblur_Kernel_WindowSize.get()),
                )

                # create a mask with the same size as the sub-image, filled with zeros
                mask = np.zeros_like(sub3)
                mask2 = np.zeros_like(sub4)

                # create a circle on the mask with the same size as the sub-image
                cv2.circle(mask, (radius, radius), radius, (255, 255, 255), -1)
                cv2.circle(mask2, (radius, radius), radius, (255, 255, 255), -1)

                # apply the mask to the blurred image
                blurred_roi = cv2.bitwise_and(wiener_img, mask)
                blurred_roi2 = cv2.bitwise_and(wiener_img2, mask2)

                # paste blurred ROI on the original image
                I[y : y + h, x : x + w] = blurred_roi
                save[y : y + h, x : x + w] = blurred_roi2

                canvasRemake(I)
        elif choice2 == "Gaussian Blurring":
            for circle in ROIs2:
                # unpack the circle parameters
                center, radius = circle

                # calculate the bounding box for the circle
                x, y = int(center[0] - radius), int(center[1] - radius)
                w, h = int(2 * radius), int(2 * radius)

                # crop the image due to the current circle
                sub3 = I[y : y + h, x : x + w]
                sub4 = save[y : y + h, x : x + w]

                # apply DeBlur on cropped area
                wiener_img = cv2.fastNlMeansDenoising(
                    sub3,
                    None,
                    int(Deblur_Kernel_StrengthDenoising.get()),
                    int(Deblur_Kernel_StrengthColor.get()),
                    int(Deblur_Kernel_WindowSize.get()),
                )
                wiener_img2 = cv2.fastNlMeansDenoising(
                    sub4,
                    None,
                    int(Deblur_Kernel_StrengthDenoising.get()),
                    int(Deblur_Kernel_StrengthColor.get()),
                    int(Deblur_Kernel_WindowSize.get()),
                )

                # create a mask with the same size as the sub-image, filled with zeros
                mask = np.zeros_like(sub3)
                mask2 = np.zeros_like(sub4)

                # create a circle on the mask with the same size as the sub-image
                cv2.circle(mask, (radius, radius), radius, (255, 255, 255), -1)
                cv2.circle(mask2, (radius, radius), radius, (255, 255, 255), -1)

                # apply the mask to the blurred image
                blurred_roi = cv2.bitwise_and(wiener_img, mask)
                blurred_roi2 = cv2.bitwise_and(wiener_img2, mask2)

                # paste blurred ROI on the original image
                I[y : y + h, x : x + w] = blurred_roi
                save[y : y + h, x : x + w] = blurred_roi2

                canvasRemake(I)
        elif choice2 == "Median Blurring":
            for circle in ROIs2:
                # unpack the circle parameters
                center, radius = circle

                # calculate the bounding box for the circle
                x, y = int(center[0] - radius), int(center[1] - radius)
                w, h = int(2 * radius), int(2 * radius)

                # crop the image due to the current circle
                sub3 = I[y : y + h, x : x + w]
                sub4 = save[y : y + h, x : x + w]

                # apply DeBlur on cropped area
                wiener_img = cv2.fastNlMeansDenoising(
                    sub3,
                    None,
                    int(Deblur_Kernel_StrengthDenoising.get()),
                    int(Deblur_Kernel_StrengthColor.get()),
                    int(Deblur_Kernel_WindowSize.get()),
                )
                wiener_img2 = cv2.fastNlMeansDenoising(
                    sub4,
                    None,
                    int(Deblur_Kernel_StrengthDenoising.get()),
                    int(Deblur_Kernel_StrengthColor.get()),
                    int(Deblur_Kernel_WindowSize.get()),
                )

                # create a mask with the same size as the sub-image, filled with zeros
                mask = np.zeros_like(sub3)
                mask2 = np.zeros_like(sub4)

                # create a circle on the mask with the same size as the sub-image
                cv2.circle(mask, (radius, radius), radius, (255, 255, 255), -1)
                cv2.circle(mask2, (radius, radius), radius, (255, 255, 255), -1)

                # apply the mask to the blurred image
                blurred_roi = cv2.bitwise_and(wiener_img, mask)
                blurred_roi2 = cv2.bitwise_and(wiener_img2, mask2)

                # paste blurred ROI on the original image
                I[y : y + h, x : x + w] = blurred_roi
                save[y : y + h, x : x + w] = blurred_roi2

                canvasRemake(I)
        elif choice2 == "Bilateral Filtering":
            for circle in ROIs2:
                # unpack the circle parameters
                center, radius = circle

                # calculate the bounding box for the circle
                x, y = int(center[0] - radius), int(center[1] - radius)
                w, h = int(2 * radius), int(2 * radius)

                # crop the image due to the current circle
                sub3 = I[y : y + h, x : x + w]
                sub4 = save[y : y + h, x : x + w]

                # apply DeBlur on cropped area
                wiener_img = cv2.fastNlMeansDenoising(
                    sub3,
                    None,
                    int(Deblur_Kernel_StrengthDenoising.get()),
                    int(Deblur_Kernel_StrengthColor.get()),
                    int(Deblur_Kernel_WindowSize.get()),
                )
                wiener_img2 = cv2.fastNlMeansDenoising(
                    sub4,
                    None,
                    int(Deblur_Kernel_StrengthDenoising.get()),
                    int(Deblur_Kernel_StrengthColor.get()),
                    int(Deblur_Kernel_WindowSize.get()),
                )
                # create a mask with the same size as the sub-image, filled with zeros
                mask = np.zeros_like(sub3)
                mask2 = np.zeros_like(sub4)

                # create a circle on the mask with the same size as the sub-image
                cv2.circle(mask, (radius, radius), radius, (255, 255, 255), -1)
                cv2.circle(mask2, (radius, radius), radius, (255, 255, 255), -1)

                # apply the mask to the blurred image
                blurred_roi = cv2.bitwise_and(wiener_img, mask)
                blurred_roi2 = cv2.bitwise_and(wiener_img2, mask2)

                # paste blurred ROI on the original image
                I[y : y + h, x : x + w] = blurred_roi
                save[y : y + h, x : x + w] = blurred_roi2

                canvasRemake(I)


def sharpen():
    global I, ROIs, ROIs2, center, EnNeibor, EnSigCol, EnSigSpa, EnKerX, EnKerY, EnKerX1, EnKerY1, EnSigmX, EnSigmY, EnKerX2
    choice2 = default_roi.get()
    if choice2 == "Rectangle ROIs":
        for box in ROIs:
            # unpack each box
            x, y, w, h = [d for d in box]

            # crop the image due to the current box
            sub = I[y : y + h, x : x + w]
            sub2 = save[y : y + h, x : x + w]
            # apply Blur on cropped area
            sharpened = cv2.filter2D(sub, -1, Sharpen_Kernel)
            sharpened2 = cv2.filter2D(sub2, -1, Sharpen_Kernel)

            # paste blurred image on the original image
            I[y : y + h, x : x + w] = sharpened
            save[y : y + h, x : x + w] = sharpened2

            canvasRemake(I)

    elif choice2 == "Circle ROIs":
        for circle in ROIs2:
            # unpack the circle parameters
            center, radius = circle

            # calculate the bounding box for the circle
            x, y = int(center[0] - radius), int(center[1] - radius)
            w, h = int(2 * radius), int(2 * radius)

            # crop the image due to the current circle
            sub3 = I[y : y + h, x : x + w]
            sub4 = save[y : y + h, x : x + w]

            # apply Blur on cropped area
            sharpened = cv2.filter2D(sub3, -1, Sharpen_Kernel)
            sharpened2 = cv2.filter2D(sub4, -1, Sharpen_Kernel)

            # create a mask with the same size as the sub-image, filled with zeros
            mask = np.zeros_like(sub3)
            mask2 = np.zeros_like(sub4)

            # create a circle on the mask with the same size as the sub-image
            cv2.circle(mask, (radius, radius), radius, (255, 255, 255), -1)
            cv2.circle(mask2, (radius, radius), radius, (255, 255, 255), -1)

            # apply the mask to the blurred image
            sharpened_roi = cv2.bitwise_and(sharpened, mask)
            sharpened_roi2 = cv2.bitwise_and(sharpened2, mask2)

            # paste blurred ROI on the original image
            I[y : y + h, x : x + w] = sharpened_roi
            save[y : y + h, x : x + w] = sharpened_roi2

            canvasRemake(I)


def erase():
    global I, I_reset, ROIs, ROIs2, center, EnNeibor, EnSigCol, EnSigSpa, EnKerX, EnKerY, EnKerX1, EnKerY1, EnSigmX, EnSigmY, EnKerX2
    choice2 = default_roi.get()
    if choice2 == "Rectangle ROIs":
        for box in ROIs:
            # unpack each box
            x, y, w, h = [d for d in box]

            sub = I_reset[y : y + h, x : x + w]
            sub2 = I_reset[y : y + h, x : x + w]
            # paste reset image on the image
            I[y : y + h, x : x + w] = sub
            save[y : y + h, x : x + w] = sub2

            canvasRemake(I)

    elif choice2 == "Circle ROIs":
        for circle in ROIs2:
            # unpack the circle parameters
            center, radius = circle

            # calculate the bounding box for the circle
            x, y = int(center[0] - radius), int(center[1] - radius)
            w, h = int(2 * radius), int(2 * radius)

            # crop the image due to the current circle
            sub3 = I_reset[y : y + h, x : x + w]
            sub4 = I_reset[y : y + h, x : x + w]

            # paste reset image on the original image
            I[y : y + h, x : x + w] = sub3
            save[y : y + h, x : x + w] = sub4

            canvasRemake(I)


# # Define global variables
# drawing = False  # True if mouse is pressed
# mode = True  # True if draw rectangle, False if erase
# ix, iy = -1, -1
# brush_size = 20
# blur_kernel_size = 21

# # mouse callback function
# def erase_roi(event, x, y, flags, param):
#     global ix, iy, drawing, mode, I

#     if event == cv2.EVENT_LBUTTONDOWN:
#         drawing = True
#         ix, iy = x, y

#     elif event == cv2.EVENT_MOUSEMOVE:
#         if drawing == True:
#             if mode == True:
#                 cv2.rectangle(I, (ix, iy), (x, y), (0, 255, 0), 2)
#             else:
#                 cv2.circle(I, (x, y), brush_size, (255, 0, 0), 2)

#     elif event == cv2.EVENT_LBUTTONUP:
#         drawing = False
#         if mode == True:
#             cv2.rectangle(I, (ix, iy), (x, y), (0, 255, 0), 2)
#             roi = I[iy:y, ix:x]
#             blurred_roi = cv2.GaussianBlur(
#                 roi, (blur_kernel_size, blur_kernel_size), 0)
#             IconPhoto[iy:y, ix:x] = blurred_roi
#         else:
#             cv2.circle(I, (x, y), brush_size, (255, 0, 0), 2)


# def erase():
#     global I, ROIs, mode
#     cv2.namedWindow('Erase')
#     cv2.setMouseCallback('Erase', erase_roi)
#     # for box in ROIs:
#     #     # unpack each box
#     #     x, y, w, h = [d for d in box]

#     #     # crop the image due to the current box
#     #     sub = I[y:y+h, x:x+w]
#     while (1):
#         cv2.imshow('Erase', I)
#         k = cv2.waitKey(1) & 0xFF
#         if k == ord('m'):
#             mode = not mode
#         elif k == ord('s'):
#             cv2.imwrite('image.png', I)
#         elif k == 27:
#             break

#     canvasRemake(I)


def BoxBlurFrame(BOXWINDOW):
    global EnKerX, EnKerY
    BOXFrame = Frame(BOXWINDOW, width=50, height=50, bg="#444654")
    BOXFrame.grid(row=2, column=0, padx=10, pady=10)

    TitleL = Label(
        BOXFrame, text="Averaging Blur Options:", bg="#444654", fg="white"
    ).grid(row=0, column=0)
    KerX = Label(BOXFrame, text="KERNEL X:", bg="#444654", fg="white").grid(
        row=1, column=0
    )
    KerY = Label(BOXFrame, text="KERNEL Y:", bg="#444654", fg="white").grid(
        row=2, column=0
    )

    EnKerX = Entry(BOXFrame, textvariable=Kernel_boxX)

    EnKerX.grid(row=1, column=1)

    EnKerY = Entry(BOXFrame, textvariable=Kernel_boxY)

    EnKerY.grid(row=2, column=1)


def GaussianBlurFrame(GAUSWINDOW):
    global EnKerX1, EnKerY1, EnSigmX, EnSigmY

    GAUSFrame = Frame(GAUSWINDOW, width=50, height=50, bg="#444654")
    GAUSFrame.grid(row=3, column=0, padx=10, pady=10)

    TitleL = Label(
        GAUSFrame, text="Gaussian Blur Options:", bg="#444654", fg="white"
    ).grid(row=0, column=0)
    KerX1 = Label(GAUSFrame, text="KERNEL X:", bg="#444654", fg="white").grid(
        row=1, column=0
    )
    KerY1 = Label(GAUSFrame, text="KERNEL Y:", bg="#444654", fg="white").grid(
        row=2, column=0
    )
    SIGMX = Label(GAUSFrame, text="SIGMA X:", bg="#444654", fg="white").grid(
        row=3, column=0
    )
    SIGMY = Label(GAUSFrame, text="SIGMA Y:", bg="#444654", fg="white").grid(
        row=4, column=0
    )

    EnKerX1 = Entry(GAUSFrame, textvariable=Gauss_KernelX)

    EnKerX1.grid(row=1, column=1)

    EnKerY1 = Entry(GAUSFrame, textvariable=Gauss_KernelY)

    EnKerY1.grid(row=2, column=1)

    EnSigmX = Entry(GAUSFrame, textvariable=Gauss_SigX)

    EnSigmX.grid(row=3, column=1)

    EnSigmY = Entry(GAUSFrame, textvariable=Gauss_SigY)

    EnSigmY.grid(row=4, column=1)


def MedianBlurFrame(MEDWINDOW):
    global EnKerX2

    MEDFrame = Frame(MEDWINDOW, width=50, height=50, bg="#444654")
    MEDFrame.grid(row=4, column=0, padx=10, pady=10)

    TitleL = Label(
        MEDFrame, text="Median Blur Options:", bg="#444654", fg="white"
    ).grid(row=0, column=0)
    KerX2 = Label(MEDFrame, text="Aperture Size:", bg="#444654", fg="white").grid(
        row=1, column=0
    )

    EnKerX2 = Entry(MEDFrame, textvariable=Median_KernelX)

    EnKerX2.grid(row=1, column=1)


def BilateralBlurFrame(BiWindow):
    global EnNeibor, EnSigCol, EnSigSpa

    BiFrame = Frame(BiWindow, width=50, height=50, bg="#444654")
    BiFrame.grid(row=5, column=0, padx=10, pady=10)

    TitleL = Label(
        BiFrame, text="Bilateral Blur Options:", bg="#444654", fg="white"
    ).grid(row=0, column=0)
    NeigSize = Label(BiFrame, text="Neighborhood Size:", bg="#444654", fg="white").grid(
        row=1, column=0
    )
    SigCOlor = Label(BiFrame, text="Sigma Color:", bg="#444654", fg="white").grid(
        row=2, column=0
    )
    SigSpace = Label(BiFrame, text="Sigma Space:", bg="#444654", fg="white").grid(
        row=3, column=0
    )

    EnNeibor = Entry(BiFrame, textvariable=Bi_Nei)
    EnNeibor.grid(row=1, column=1)

    EnSigCol = Entry(BiFrame, textvariable=Bi_Color)
    EnSigCol.grid(row=2, column=1)

    EnSigSpa = Entry(BiFrame, textvariable=Bi_Space)
    EnSigSpa.grid(row=3, column=1)


def DeblurFrame(DeblurWindow):
    global EnNeibor, EnSigCol, EnSigSpa

    DeblurFrame = Frame(DeblurWindow, width=50, height=50, bg="#444654")
    DeblurFrame.grid(row=6, column=0, padx=10, pady=10)

    TitleL = Label(DeblurFrame, text="DeBlur Options:", bg="#444654", fg="white").grid(
        row=0, column=0
    )
    StrDen = Label(
        DeblurFrame, text="Strength Denoising:", bg="#444654", fg="white"
    ).grid(row=1, column=0)
    StrCol = Label(DeblurFrame, text="Strength Color:", bg="#444654", fg="white").grid(
        row=2, column=0
    )
    WinSize = Label(DeblurFrame, text="Window Size:", bg="#444654", fg="white").grid(
        row=3, column=0
    )

    DeStrengthDen = Entry(DeblurFrame, textvariable=Deblur_Kernel_StrengthDenoising)
    DeStrengthDen.grid(row=1, column=1)

    DeStrengthCol = Entry(DeblurFrame, textvariable=Deblur_Kernel_StrengthColor)
    DeStrengthCol.grid(row=2, column=1)

    DeWindowSi = Entry(DeblurFrame, textvariable=Deblur_Kernel_WindowSize)
    DeWindowSi.grid(row=3, column=1)


winde1 = 0


def on_closing1():
    global winde1
    winde1.destroy()
    winde1 = 0


def Blur_Menu():
    global default_blur, winde1

    BLMenu = Toplevel(root)
    winde1 = BLMenu
    BLMenu.protocol("WM_DELETE_WINDOW", on_closing1)
    MenuFrame = Frame(BLMenu, width=200, height=200, bg="#343541")
    MenuFrame.grid(row=0, column=0, padx=5, pady=5)
    BLMenu.resizable(False, False)

    BoxBlurFrame(MenuFrame)
    GaussianBlurFrame(MenuFrame)
    MedianBlurFrame(MenuFrame)
    BilateralBlurFrame(MenuFrame)
    DeblurFrame(MenuFrame)

    Dropl = Label(
        MenuFrame, text="Active Blur Algorithm:", bg="#444654", fg="white"
    ).grid(row=0, column=0, sticky="w", padx=5, pady=3, ipadx=10)
    drop = OptionMenu(MenuFrame, default_blur, *Blur_options).grid(
        row=1, column=0, sticky="w", padx=5, pady=3, ipadx=10
    )


def SeeIfOpen():
    if winde1 == 0:
        Blur_Menu()
    else:
        winde1.lift()


def camera():
    global save, I, ROIs, ROIs2
    ROIs.clear()
    ROIs2.clear()
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        key = cv2.waitKey(1) & 0xFF
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Image Smoothing", "Error: No camera was found")
            break

        h, l, c = frame.shape
        picture = frame.copy()

        cv2.putText(
            img=frame,
            text="Press Space to take picture",
            org=(10, 17),
            fontFace=cv2.FONT_HERSHEY_DUPLEX,
            fontScale=0.5,
            color=(255, 255, 255),
            thickness=1,
        )
        cv2.putText(
            img=frame,
            text="Press Q to quit",
            org=(l - 135, h - 10),
            fontFace=cv2.FONT_HERSHEY_DUPLEX,
            fontScale=0.5,
            color=(255, 255, 255),
            thickness=1,
        )
        cv2.imshow("Camera", frame)

        if key == ord(" "):
            canvasRemake(picture)
            save = picture.copy()
            I = picture
            z = cv2.cvtColor(picture, cv2.COLOR_BGR2RGB)

            cv2.destroyWindow("Camera")
            break
        if key == ord("q"):
            cv2.destroyWindow("Camera")
            break

    cap.release()


winde2 = 0


def on_closing2():
    global winde2
    winde2.destroy()
    winde2 = 0


def SeeROIs():
    if winde2 == 0:
        ROIs_Menu()
    else:
        winde2.lift()


def ROIs_Menu():
    global default_roi, winde2

    ROIMenu = Toplevel(root)
    winde2 = ROIMenu
    ROIMenu.protocol("WM_DELETE_WINDOW", on_closing2)
    MenuFrame = Frame(ROIMenu, width=200, height=200, bg="#343541")
    MenuFrame.grid(row=0, column=0, padx=5, pady=5)
    ROIMenu.resizable(False, False)

    Drop2 = Label(MenuFrame, text="Active ROI:", bg="#444654", fg="white").grid(
        row=0, column=0, sticky="w", padx=5, pady=3, ipadx=10
    )
    drop = OptionMenu(MenuFrame, default_roi, *ROIs_options).grid(
        row=1, column=0, sticky="w", padx=5, pady=3, ipadx=10
    )


# Buttons
# tools
Import_button = Button(
    tools_sidebar,
    text="Import",
    relief="ridge",
    bg="#444654",
    fg="white",
    command=import_file,
).grid(row=0, column=0, padx=10, pady=10, ipadx=10, sticky="news")
ROIs_Button = Button(
    tools_sidebar,
    text="ROIS",
    relief="ridge",
    bg="#444654",
    fg="white",
    command=start_crop,
).grid(row=1, column=0, padx=10, pady=10, ipadx=10, sticky="news")
Camera_Button = Button(
    tools_sidebar,
    text="Camera",
    relief="ridge",
    bg="#444654",
    fg="white",
    command=camera,
).grid(row=2, column=0, padx=10, pady=10, ipadx=10, sticky="news")
Export_Button = Button(
    tools_sidebar,
    text="Export",
    relief="ridge",
    bg="#444654",
    fg="white",
    command=export_window,
).grid(row=3, column=0, padx=10, pady=10, ipadx=10, sticky="news")
ROIs_Options_Button = Button(
    tools_sidebar,
    text="Options",
    relief="ridge",
    bg="#444654",
    fg="white",
    command=SeeROIs,
).grid(row=4, column=0, padx=10, pady=10, ipadx=10, sticky="news")

# filters
Blur_Button = Button(
    filters_sidebar, text="Blur", relief="ridge", bg="#444654", fg="white", command=blur
).grid(row=0, column=0, padx=10, pady=10, ipadx=10, sticky="news")
Deblur_Button = Button(
    filters_sidebar,
    text="Deblur",
    relief="ridge",
    bg="#444654",
    fg="white",
    command=deblur,
).grid(row=1, column=0, padx=10, pady=10, ipadx=10, sticky="news")
Sharpen_Button = Button(
    filters_sidebar,
    text="Sharpen",
    relief="ridge",
    bg="#444654",
    fg="white",
    command=sharpen,
).grid(row=2, column=0, padx=10, pady=10, ipadx=10, sticky="news")
Erase_Button = Button(
    filters_sidebar,
    text="Erase",
    relief="ridge",
    bg="#444654",
    fg="white",
    command=erase,
).grid(row=3, column=0, padx=10, pady=10, ipadx=10, sticky="news")
Blur_Options_Button = Button(
    filters_sidebar,
    text="Options",
    relief="ridge",
    bg="#444654",
    fg="white",
    command=SeeIfOpen,
).grid(row=4, column=0, padx=10, pady=10, ipadx=10, sticky="news")


# Run App
root.mainloop()
