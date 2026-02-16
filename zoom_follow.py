import obspython as obs
import ctypes

# --- GLOBAL VARIABLES ---
source_name = ""
zoom_level = 1.5      # How much to zoom in (1.5 = 150%)
smoothness = 0.08     # Lower = Smoother, Higher = Snappier
follow_active = True

# Camera position (used for smoothing)
cam_x = 0.0
cam_y = 0.0

# Screen Size (Default 1920x1080, updates automatically)
screen_w = 1920
screen_h = 1080

# Windows API for Mouse
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

# --- HELPER FUNCTIONS ---

def get_mouse_pos():
    """Get the raw global mouse position."""
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

def lerp(start, end, alpha):
    """Linear Interpolation for smooth movement."""
    return start + (end - start) * alpha

# --- OBS SCRIPT FUNCTIONS ---

def script_description():
    return "Dynamic Zoom & Follow Camera\n\nZooms into a Display Capture source and keeps the mouse centered.\n\nUsage:\n1. Add a 'Display Capture' source.\n2. Select it below.\n3. Adjust Zoom and Smoothness."

def script_properties():
    props = obs.obs_properties_create()
    
    # Dropdown to select the Display Capture source
    p = obs.obs_properties_add_list(props, "source", "Select Display Source", 
                                    obs.OBS_COMBO_TYPE_EDITABLE, 
                                    obs.OBS_COMBO_FORMAT_STRING)
    
    # Populate dropdown with current sources
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            name = obs.obs_source_get_name(source)
            obs.obs_property_list_add_string(p, name, name)
        obs.source_list_release(sources)

    # Sliders for settings
    obs.obs_properties_add_float_slider(props, "zoom", "Zoom Level (x)", 1.0, 4.0, 0.1)
    obs.obs_properties_add_float_slider(props, "smoothness", "Smoothness (Low=Slow)", 0.01, 0.5, 0.01)
    
    return props

def script_update(settings):
    """Called when settings change."""
    global source_name, zoom_level, smoothness
    source_name = obs.obs_data_get_string(settings, "source")
    zoom_level = obs.obs_data_get_double(settings, "zoom")
    smoothness = obs.obs_data_get_double(settings, "smoothness")

def script_tick(seconds):
    """Called every frame to update position."""
    global cam_x, cam_y, screen_w, screen_h
    
    if not source_name:
        return

    # 1. Find the Source in the Current Scene
    current_scene = obs.obs_frontend_get_current_scene()
    scene = obs.obs_scene_from_source(current_scene)
    scene_item = obs.obs_scene_find_source_recursive(scene, source_name)
    
    if scene_item:
        # 2. Update Resolution (One-time check usually)
        target_source = obs.obs_sceneitem_get_source(scene_item)
        if target_source:
            w = obs.obs_source_get_width(target_source)
            h = obs.obs_source_get_height(target_source)
            if w > 0 and h > 0:
                screen_w = w
                screen_h = h

        # 3. Get Target Mouse Position
        mx, my = get_mouse_pos()
        
        # 4. Smooth the Camera Movement
        cam_x = lerp(cam_x, mx, smoothness)
        cam_y = lerp(cam_y, my, smoothness)

        # 5. Calculate Center Offset
        # We want the mouse (cam_x, cam_y) to be at the center of the canvas (screen_w/2, screen_h/2)
        center_x = screen_w / 2
        center_y = screen_h / 2
        
        # The new position of the source needs to be offset so the mouse is centered
        # Formula: SourcePos = Center - (MousePos * Zoom)
        new_x = center_x - (cam_x * zoom_level)
        new_y = center_y - (cam_y * zoom_level)

        # 6. Apply Scale (Zoom)
        scale = obs.vec2()
        scale.x = zoom_level
        scale.y = zoom_level
        obs.obs_sceneitem_set_scale(scene_item, scale)

        # 7. Apply Position
        pos = obs.vec2()
        pos.x = new_x
        pos.y = new_y
        obs.obs_sceneitem_set_pos(scene_item, pos)

    obs.obs_source_release(current_scene)