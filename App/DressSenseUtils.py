import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import sklearn
from sklearn.cluster import KMeans
from collections import Counter
import cv2
import streamlit as st
from PIL import ImageColor, Image
import argparse
import os
#Reading csv file with pandas
csv = pd.read_csv('new_colors.csv')

plt.style.use('ggplot')
plt.rcParams['font.family'] = 'sans-serif' 
plt.rcParams['font.serif'] = 'Ubuntu' 
plt.rcParams['font.monospace'] = 'Ubuntu Mono' 
plt.rcParams['font.size'] = 14 
plt.rcParams['axes.labelsize'] = 12 
plt.rcParams['axes.labelweight'] = 'bold' 
plt.rcParams['axes.titlesize'] = 12 
plt.rcParams['xtick.labelsize'] = 12 
plt.rcParams['ytick.labelsize'] = 12 
plt.rcParams['legend.fontsize'] = 12 
plt.rcParams['figure.titlesize'] = 12 
plt.rcParams['image.cmap'] = 'jet' 
plt.rcParams['image.interpolation'] = 'none' 
plt.rcParams['figure.figsize'] = (10, 10
                                 ) 
plt.rcParams['axes.grid']=False
plt.rcParams['lines.linewidth'] = 2 
plt.rcParams['lines.markersize'] = 8
colors = ['xkcd:pale orange', 'xkcd:sea blue', 'xkcd:pale red', 'xkcd:sage green', 'xkcd:terra cotta', 'xkcd:dull purple', 'xkcd:teal', 'xkcd: goldenrod', 'xkcd:cadet blue',
'xkcd:scarlet']

'''Reading image in RGB color space'''
def get_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image
def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

'''Run the Kmeans algorithm on the uploaded image in order to get the top 10 colors that recognized in the image'''
def run_KMeans(image_path):
    # uploaded_image_name = list(upload.value.keys())[0]
    # st.write("Running KMeans algorithm")
    st.write(f"Running KMeans algorithm for {image_path}")
    image = get_image(image_path)
    number_of_colors = 10
    modified_image = image.reshape(image.shape[0]*image.shape[1], 3)
    clf = KMeans(n_clusters = number_of_colors)
    labels = clf.fit_predict(modified_image)
    return clf, labels


'''function to calculate minimum distance from all colors and get the most matching color'''
def getColorName(val,val_type):
    #type: # RGB or hex
    if val_type == 'hex':
        my_rgb = ImageColor.getcolor(str(val), "RGB")
    else:
        my_rgb = val
    R = my_rgb[0]
    G = my_rgb[1]
    B = my_rgb[2]
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
            tname = csv.loc[i,"tone"]
    return [cname, tname]

'''The get_sorted_dict_of_colors() function is used to sort the colors present in an image by their frequency of occurrence. 
the function iterates through the colors_labels_by_name list and color_values list, where it updates the values of the
dict_colors_values dictionary by adding the appernces values of the color_values list to the corresponding color
in the colors_labels_by_name list.
Finally, the function sorts the dictionary in descending order by the values of the dictionary, and returns the sorted
dictionary.'''
def get_sorted_dict_of_colors(image_path):
    clf, labels = run_KMeans(image_path)
    counts = Counter(labels)
    center_colors = clf.cluster_centers_

    # We get ordered colors by iterating through the keys
    ordered_colors = [center_colors[i] for i in counts.keys()]

    hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
    rgb_colors = [ordered_colors[i] for i in counts.keys()]
    colors_labels_by_name = [getColorName(color,'hex')[0] for color in hex_colors]
    colors_labels = [getColorName(color,'hex') for color in hex_colors]
    colors_values = list(counts.values())
    #This code is creating a dictionary that will store the counts of colors present in the uploaded image.
    allowed_colors = ['Black', 'White', 'Blue', 'Purple', 'Red', 'Pink', 'Green', 'Yellow', 'Orange', 'Brown', 'Gray', 'Dark Red',
                      'Beige','Light Blue']
    bucket_colors = [0]*len(allowed_colors)
    dict_colors_values = {allowed_colors[i]: bucket_colors[i] for i in range(len(allowed_colors))}

    for count, color in enumerate(colors_labels_by_name):
        dict_colors_values[color] += colors_values[count]
    #sort the dict in descending order
    sorted_colors_dict = {k: v for k, v in sorted(dict_colors_values.items(), key=lambda item: item[1], reverse=True)}
    return sorted_colors_dict, colors_labels_by_name, rgb_colors


def get_colors_shapes(image_path, sorted_colors_dict, colors_labels1):
    main_folder = os.path.dirname(os.path.abspath("DressSenseUtils"))
    colors_folder = os.path.join(main_folder, "Colors")
    paths = []
    # sorted_colors_dict = sorted_colors_dict1()
    for color in sorted_colors_dict.keys():
        if sorted_colors_dict[color]!=0:
            path = os.path.join(colors_folder, color + '.jpg')
            paths.append(path)

    wdgs = [plt.imread(path) for path in paths]
    space = 20
    total_width = sum(wgd.shape[1] + space for wgd in wdgs) - space
    max_height = max(wgd.shape[0] for wgd in wdgs)

    new_image = np.zeros((max_height, total_width, 3), dtype=np.uint8)
    new_image.fill(255)

    x_offset = 0
    for wdg in wdgs:
        height, width, _ = wdg.shape
        if height < max_height:
            top_padding = (max_height - height) // 2
            bottom_padding = max_height - height - top_padding
            wdg = np.pad(wdg, [(top_padding, bottom_padding), (0, 0), (0, 0)], mode='constant', constant_values=255)
        new_image[:wdg.shape[0], x_offset:x_offset+wdg.shape[1], :] = wdg
        x_offset += wdg.shape[1] + space
    plt.axis("off")
    # plt.title('These are the colors that appear in your closet in descending order')
    plt.title(f'These are the colors that appear in {image_path} image in descending order')
    plt.imshow(new_image)
    st.pyplot(plt)
    # plt.show()



def inthreshold(array):
    count = 0
    for i in range(len(array)):
        if array[i]>=-12 and array[i]<=12:
            count=count+1
    return count

'''recognize the location of the tone'''
def show_color_byInx(col_indexes, mark_color, image, rgb_colors):
    for col_index in col_indexes:
        color = col_index
        sub_image = (image-rgb_colors[color])
        ZEROS_VALUES = []
        COUNT = []
        for i in range(len(sub_image)):
            for j in range(len(sub_image[i])):
                e = sub_image[i,j]
                count = inthreshold(e)
                COUNT.append(count)
                if count==2:
                    ZEROS_VALUES.append([i,j])
        color_arr=(np.zeros((16,16,3))+rgb_colors[color]).astype(int)
        normalized = sub_image - sub_image.min()
        normalized = ((sub_image/sub_image.max())*255).astype(int)
        ZEROS_IMAGE = image.copy()
        for i in range(len(ZEROS_VALUES)):
            # marking the relevant pixels in the mark color
            ZEROS_IMAGE[ZEROS_VALUES[i][0],ZEROS_VALUES[i][1],:] = mark_color
    col1, col2,= st.columns([5, 5])
    with col1:
        st.subheader("Selected Color")
        st.image(ZEROS_IMAGE.astype(int), use_column_width=True)
    with col2:

        st.subheader("Original Image")
        st.image(image, use_column_width=True)

'''recognize the location of the desire color (includes all the tones of the color)'''
def show_color(color, image_path, sorted_dict_of_colors, rgb_colors):
    image = get_image(image_path)
    indices = [i for i, x in enumerate(sorted_dict_of_colors) if x == color]
    lst_black_mark = ['White','Yellow','Orange','Beige','Light Blue','Green']
    lst_white_mark = ['Black','Purple','Red','Pink','Brown','Dark Red','Gray','Blue']
    if color in lst_black_mark:
        mark_color = [0,0,0] #black
    elif color in lst_white_mark:
        mark_color = [255,255,255] #white
    return show_color_byInx(indices, mark_color, image, rgb_colors)


# ### This is the first graph that the Kmeans algorithm provided us. We made the above changes in order to display the colors in a way that couls be accessive to color blind users.
# this is an exmaple running on the folded_shirts.jpg image

# In[ ]:


# '''Run the Kmeans algorithm on the uploaded image in order to get the top 10 colors that recognized in the image'''
# def run_KMeans():
#     uploaded_image_name = list(upload.value.keys())[0]
#     image = get_image(uploaded_image_name)
#     number_of_colors = 10
#     modified_image = image.reshape(image.shape[0]*image.shape[1], 3)
#     clf = KMeans(n_clusters = number_of_colors)
#     labels = clf.fit_predict(modified_image)
#     return clf, labels
#
# def show_graph():
#     clf, labels = run_KMeans()
#     counts = Counter(labels)
#     center_colors = clf.cluster_centers_
#
#     # We get ordered colors by iterating through the keys
#     ordered_colors = [center_colors[i] for i in counts.keys()]
#     hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
#     rgb_colors = [ordered_colors[i] for i in counts.keys()]
#     colors_labels = [getColorName(color,'hex')[0] for color in hex_colors]
#     tones_labels = [getColorName(color,'hex')[1] for color in hex_colors]
#     plt.title('Colors Tones Detection ($n=20$)', fontsize=20)
#     plt.pie(counts.values(), labels = tones_labels, colors = hex_colors)
#
#
# # In[ ]:




