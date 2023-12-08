import QtQuick
//import QtQuick.Timeline
import QtQuick.Controls
import org.ekart.DashboardController 1.0



Button {
    id: closecamera
    text: "Close Camera"
    anchors.horizontalCenter: parent.horizontalCenter
    anchors.top: parent.top
    font.family: "Haettenschweiler"
    font.pixelSize: 22
    hoverEnabled: false
    onClicked: stateGroup.state = "default"

    background: Image {
        id: background
        source: "../images/closeCam.png"
        fillMode: Image.PreserveAspectFit
    }
}
