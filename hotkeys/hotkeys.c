#include <X11/Xlib.h>
#include <X11/keysym.h>
#include <stdio.h>
#include <stdlib.h>

int main() {
    Display *display;
    Window root;
    XEvent ev;

    display = XOpenDisplay(NULL);
    if (!display) {
        fprintf(stderr, "Cannot open display\n");
        return 1;
    }

    root = DefaultRootWindow(display);

    // Get keycode for 'K'
    KeyCode keycode = XKeysymToKeycode(display, XStringToKeysym("K"));

    // Modifiers: Control + Alt
    unsigned int modifiers = ControlMask | Mod1Mask; // Mod1 = Alt on most systems

    // Grab the key
    XGrabKey(display, keycode, modifiers, root, True, GrabModeAsync, GrabModeAsync);


    XSelectInput(display, root, KeyPressMask);

    printf("Listening for Ctrl+Alt+K...\n");

    while (1) {
        XNextEvent(display, &ev);
        if (ev.type == KeyPress) {
            XKeyEvent xkey = ev.xkey;
            if (xkey.keycode == keycode && (xkey.state & (ControlMask | Mod1Mask))) {
                printf("Ctrl+Alt+K pressed! Launching...\n");
                system("gedit &");
            }
        }
    }

    XCloseDisplay(display);
    return 0;
}
