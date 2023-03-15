#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/alineitudor/Licenta-git/src/bluerov_ros_playground"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/alineitudor/Licenta-git/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/alineitudor/Licenta-git/install/lib/python2.7/dist-packages:/home/alineitudor/Licenta-git/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/alineitudor/Licenta-git/build" \
    "/usr/bin/python2" \
    "/home/alineitudor/Licenta-git/src/bluerov_ros_playground/setup.py" \
     \
    build --build-base "/home/alineitudor/Licenta-git/build/bluerov_ros_playground" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/alineitudor/Licenta-git/install" --install-scripts="/home/alineitudor/Licenta-git/install/bin"
