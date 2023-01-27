import streamlit as st
from streamlit_option_menu import option_menu
from st_clickable_images import clickable_images
from DressSenseUtils import get_colors_shapes, get_sorted_dict_of_colors, show_color
selected = option_menu(
    menu_title="DressSense", menu_icon="bi-palette",
    options=["Dress Me Up", "My Statistics", "About", "Settings"],
    icons=["bi-file-person-fill", "bi-clipboard-data", "info-circle-fill", "bi-gear"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
    styles={
            "container": {"padding": "10px"},
            "nav-link-selected": {"background-color": "blue"},
            "icon": {"font-size": "25px"},
            "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px","--hover-color": "#eee"}}
)
#return the sorted colors list that reconized in the image
def get_shirts_color_list():
    colors_list_shirts = []
    for count, color in enumerate(st.session_state["sorted_colors_dict_shirt"]):
        if st.session_state["sorted_colors_dict_shirt"][color] > 0:
            colors_list_shirts.append(color)

    if "colors_list_shirts" not in st.session_state:
        st.session_state["colors_list_shirts"] = colors_list_shirts
    return

def get_pants_color_list():
    colors_list_Pants = []
    for count, color in enumerate(st.session_state["sorted_colors_pants_dict"]):
        if st.session_state["sorted_colors_pants_dict"][color] > 0:
            colors_list_Pants.append(color)
    if "colors_list_pants" not in st.session_state:
        st.session_state["colors_list_pants"] = colors_list_Pants
    return

def get_shoes_color_list():
    colors_list_shoes = []
    for count, color in enumerate(st.session_state["sorted_colors_shoes_dict"]):
        if st.session_state["sorted_colors_shoes_dict"][color] > 0:
            colors_list_shoes.append(color)
    if "colors_list_shoes" not in st.session_state:
        st.session_state["colors_list_shoes"] = colors_list_shoes
    return

if selected == "Dress Me Up":
    st.title("Hello Ofra!")
    st.subheader("Get started by uploading photos of your closet, organized by clothes categories")
    st.write("Please click on each item image in order to upload corresponding image of your closet, and then click on the 'Dress Me' button")
    col1, col2 = st.columns([6, 6])

    with col1:

        clicked_shirt = clickable_images(
            [
                "https://cdn3.iconfinder.com/data/icons/clothing-set-2/64/tshirt-512.png",
            ],
            titles=["Shirt image"],
            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
            img_style={"margin": "5px", "height": "200px"},
        )

        clicked_pants = clickable_images(
            [
                "data:image/png;base64,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",
            ],
            titles=["Pants image"],
            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
            img_style={"margin": "5px", "height": "230px", "width":"250px"},
        )

        clicked_shoes = clickable_images(
            [
                "https://media.istockphoto.com/id/1205807329/vector/vector-illustration-of-shoes-isolated-on-white-background-for-kids-coloring-book.jpg?s=612x612&w=0&k=20&c=5SoZ83smabdjCYx2gMMAUjyyQ972jcrykDDpc3xK5QM="
            ],
            titles=["Shoes image"],
            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
            img_style={"margin": "5px", "height": "230px", "width": "250px"},
        )

    with col2:
        shirt=""
        pants =""
        shoes=""
        st.write("")
        if clicked_shirt > -1:
            shirt = st.file_uploader("Upload a Shirt image", type=['png', 'jpg'], key="shirt")
            if shirt:
                st.success("The image was uploaded successfully")
                if "shirt_image_name" not in st.session_state:
                    st.session_state['shirt_image_name'] = shirt.name

                # get_colors_shapes(shirt.name)
        if clicked_pants > -1:
            pants = st.file_uploader("Upload a Pants image", type=['png', 'jpg'], key="pants")
            if pants:
                st.success("The image was uploaded successfully")
                if "pants_image_name" not in st.session_state:
                    st.session_state['pants_image_name'] = pants.name
        if clicked_shoes > -1:
            shoes = st.file_uploader("Upload a Shoes image", type=['png', 'jpg'], key="shoes")
            if shoes:
                st.success("The image was uploaded successfully")
                if "shoes_image_name" not in st.session_state:
                    st.session_state['shoes_image_name'] = shoes.name

    if st.button('Dress Me'):
        st.markdown("**Tip of the day**: Experts do not suggest wearing a red shirt for first interviews.")
        #run this only if all the 3 images for the item uploaded- else print error
        if shirt and pants and shoes:
            if "shirt_image_name" in st.session_state:
                if 'ShirtChosenColor' not in st.session_state:
                    if "sorted_colors_dict_shirt" and 'colors_labels_by_name_shirt' and 'rgb_colors_shirt' not in st.session_state:
                        st.session_state["sorted_colors_dict_shirt"], st.session_state['colors_labels_by_name_shirt'], st.session_state['rgb_colors_shirt'] = get_sorted_dict_of_colors(shirt.name)
                    if "sorted_colors_dict_shirt" in st.session_state:
                        get_shirts_color_list()
        else:
            st.error("Please upload images of all the items")
    if "colors_list_shirts" in st.session_state:
        if shirt and pants and shoes:
            st.header("Shirts colors")

            get_colors_shapes(shirt.name, st.session_state["sorted_colors_dict_shirt"], st.session_state['colors_labels_by_name_shirt'])
            if 'ShirtChosenColor' not in st.session_state:

                selected_Color_shirt = st.selectbox("Choose a shirt color from the list below:",
                                                    st.session_state["colors_list_shirts"], key='ShirtChosenColor')
                st.session_state["selected_Color_shirts"] = selected_Color_shirt

            else:
                selected_Color_shirt = st.selectbox("Choose a shirt color from the list below:",
                                                    st.session_state["colors_list_shirts"], key='ShirtChosenColor')
                                                    # default=st.session_state['color'])
                st.session_state["selected_Color_shirts"] = selected_Color_shirt
                if 'rgb_colors_shirt' and 'selected_Color_shirts' and 'colors_labels_by_name_shirt' in st.session_state:
                    if selected_Color_shirt:
                        st.subheader(f"Last time you wore {selected_Color_shirt} shirt was on: Sunday")
                    show_color(st.session_state["selected_Color_shirts"], shirt.name,
                               st.session_state['colors_labels_by_name_shirt'], st.session_state['rgb_colors_shirt'])


            # mark the chosen shirt color on the uploaded image

            if "pants_image_name" in st.session_state:
                if 'PantsChosenColor' not in st.session_state:
                    if "sorted_colors_pants_dict" and 'colors_labels_by_name_pants' and 'rgb_colors_pants' not in st.session_state:
                        st.session_state["sorted_colors_pants_dict"], st.session_state[
                            'colors_labels_by_name_pants'], st.session_state["rgb_colors_pants"] = get_sorted_dict_of_colors(pants.name)
                    if "sorted_colors_pants_dict" in st.session_state:
                        get_pants_color_list()

            st.header("Pants colors")
            get_colors_shapes(pants.name, st.session_state["sorted_colors_pants_dict"], st.session_state['colors_labels_by_name_pants'])
            if 'PantsChosenColor' not in st.session_state:
                selected_Color_pants = st.selectbox("Choose a pants color from the list below:",
                                                    st.session_state["colors_list_pants"], key='PantsChosenColor')
                st.session_state["selected_Color_pants"] = selected_Color_pants
                # st.write(st.session_state["selected_Color_shirts"])
            else:
                selected_Color_pants = st.selectbox("Choose a pants color from the list below:",
                                                    st.session_state["colors_list_pants"], key='PantsChosenColor')
                                                    # default=st.session_state['color'])
                st.session_state["selected_Color_pants"] = selected_Color_pants
                # mark the chosen pants color on the uploaded image
                if 'rgb_colors_pants' and 'selected_Color_pants' and 'colors_labels_by_name_pants' in st.session_state:
                    if selected_Color_pants:
                        st.subheader(f"Last time you wore {selected_Color_pants} pants was on: Wednesday")
                    show_color(st.session_state["selected_Color_pants"], pants.name,
                               st.session_state['colors_labels_by_name_pants'], st.session_state['rgb_colors_pants'])


            if "shoes_image_name" in st.session_state:
                if 'ShoesChosenColor' not in st.session_state:
                    if "sorted_colors_shoes_dict" and 'colors_labels_by_name_shoes' not in st.session_state:
                        st.session_state["sorted_colors_shoes_dict"], st.session_state[
                            'colors_labels_by_name_shoes'], st.session_state["rgb_colors_shoes"] = get_sorted_dict_of_colors(shoes.name)
                    if "sorted_colors_shoes_dict" in st.session_state:
                        get_shoes_color_list()

            st.header("Shoes colors")
            get_colors_shapes(shoes.name, st.session_state["sorted_colors_shoes_dict"], st.session_state['colors_labels_by_name_shoes'])
            if 'ShoesChosenColor' not in st.session_state:
                selected_Color_shoes = st.selectbox("Choose a shoes color from the list below:",
                                                    st.session_state["colors_list_shoes"], key='ShoesChosenColor')
                st.session_state["selected_Color_shoes"] = selected_Color_shoes
            else:
                selected_Color_shoes = st.selectbox("Choose a shoes color from the list below:",
                                                    st.session_state["colors_list_shoes"], key='ShoesChosenColor')
                                                    # default=st.session_state['color'])
                st.session_state["selected_Color_shoes"] = selected_Color_shoes
                # mark the chosen shoes color on the uploaded image
                if 'rgb_colors_shoes' and 'selected_Color_shoes' and 'colors_labels_by_name_shoes' in st.session_state:
                    show_color(st.session_state["selected_Color_shoes"], shoes.name,
                               st.session_state['colors_labels_by_name_shoes'], st.session_state['rgb_colors_shoes'])

                    #this is an exmaple of the CheckMyOutfit output for the 3 chosen colors
                    st.header("It’s a match!")
                    st.write("Your outfit follows the rules:")
                    st.markdown("**Basic**: there is no high contrast between any colors and there is no more than one bright worn color.")
                    st.markdown("**Analogous**: the colors you chose are with the same temperature under ")

if selected == "My Statistics":
    st.image("statisticsPage.jpg", use_column_width=True)

if selected == "Settings":
    st.image("settingsPage.jpg", use_column_width=True)

if selected == "About":
    st.title("DressSense system description")
    discription_text = """
                    <strong>DressSense </strong> was created in order to assist color blind people choosing their clothes. <br>
                    Getting to know friends who are color blind, made us realize that there is a difficulty in choosing suitable colors for clothes, and that this process takes time for them.
                    Our goal is to help the color blind in this process in a visually user-friendly way.  <br><br>
                    By uploading an image of their folded clothes and choosing their wanted color, our system will mark the location of the garments in the desired color in the closet,
                    and tell the user whether his chosen colors match or not.
                        """

    st.markdown(f'<div dir="ltr"">{discription_text} </div>', unsafe_allow_html=True)
