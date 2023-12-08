import QtQuick
//import QtQuick.Timeline
import QtQuick.Controls
import org.ekart.DashboardController 1.0



Button {
    id: closecamera
    text: "Close Camera"
    width: 400
    height: 150
    anchors.horizontalCenter: parent.horizontalCenter
    anchors.top: parent.top
    anchors.topMargin: 10 // You can adjust this margin as needed
    font.family: "Haettenschweiler"
    font.pixelSize: 22
    hoverEnabled: false
    onClicked: stateGroup.state = "default"

    background: Image {
        id: background
        source: "../images/batteryPanel.png"
        fillMode: Image.PreserveAspectFit
    }
}
