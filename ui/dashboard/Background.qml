import QtQuick 2.0

Rectangle {
    width: 800  // adjust to your desired width
    height: 480 // adjust to your desired height

    Image {
        id: backgroundImage
        source: "../images/speedometer2.png" // replace with the path to your image if it's not in the same directory
        anchors.fill: parent
    }
}