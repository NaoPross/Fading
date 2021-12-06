import dearpygui.dearpygui as dpg

# Callbacks
def cb_nextpic(sender, app_data, user_data):
    dpg.set_value(texture_id, user_data['textures'][user_data['next_key']])

    # Set key for next Image. Rotate back to 1 when last image has been shown
    if user_data['next_key'] < 11:
        user_data['next_key'] = user_data['next_key']+1
    else:
        user_data['next_key'] = 1


# Load in the Logo and add it to the texture_registry
# TODO: Find out, what that thing is actually doing. It is not really clear atm.
width, height, channels, data = dpg.load_image("logo.png")
with dpg.texture_registry():
    texture_id = dpg.add_dynamic_texture(width, height, data)

# Next, load in the rest of the pictures
# Important: We are only interested in the data part here!
# Important: All the images must have the same size, because they are
#            displayed on the image that will be created from the
#            texture_id of the registry
img_dict = {}
for a in range(11):
    width, height, channels, data = dpg.load_image(f"resources\img{a+1}.png")
    img_dict[a+1] = data

img_handler_dict = {
    'next_key': 1,
    'textures': img_dict
}

with dpg.window(label="Hangman") as main_window:
    dpg.add_image(texture_id)
    dpg.add_button(label="Next IMG", callback=cb_nextpic, user_data=img_handler_dict)
    
dpg.set_primary_window(main_window, True)
dpg.start_dearpygui()