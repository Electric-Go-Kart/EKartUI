import QtQuick
import QtQuick.Controls
import org.ekart.DashboardController 1.0

Image {
    id: backgroundImage
    source: "../images/Dashboard(dark).png" // replace with the path to your image if it's not in the same directory
    anchors.centerIn: parent
    anchors.horizontalCenterOffset: -10
    fillMode: Image.PreserveAspectFit
}


