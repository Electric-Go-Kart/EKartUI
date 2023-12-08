import QtQuick
import QtQuick.Controls
import org.ekart.DashboardController 1.0

Image {
    id: backgroundImage
    source: "../images/Dashboard(dark).png" // replace with the path to your image if it's not in the same directory
    anchors.verticalCenter: parent.verticalCenter
    anchors.horizontalCenter: parent.horizontalCenter
    //anchors.horizontalCenterOffset: // Adjust this value to move the image left
    fillMode: Image.PreserveAspectFit
    fillMode: Image.PreserveAspectFit
}


