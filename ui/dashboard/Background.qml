import QtQuick
import QtQuick.Controls
import org.ekart.DashboardController 1.0

Image {
    id: backgroundImage
    source: "../images/Dashboard(dark).png" // replace with the path to your image if it's not in the same directory
    width: 800  // replace with your desired width
    height: 600 // replace with your desired height
    anchors.centerIn: parent
    fillMode: Image.PreserveAspectFit
}


