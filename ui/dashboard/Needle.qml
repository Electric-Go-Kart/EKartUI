import QtQuick
import QtQuick.Controls
import org.ekart.DashboardController 1.0

Image {
    id: needle
    source: "../images/needle.png" 
    width: 300
    height: 150
    anchors.centerIn: parent
    anchors.horizontalCenterOffset: -100 // move to the left
    anchors.verticalCenterOffset: 50 // move down
    fillMode: Image.PreserveAspectFit
    rotation: DashboardController.speed / 50 * 180 
}