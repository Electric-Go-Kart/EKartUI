import QtQuick
import QtQuick.Controls
import org.ekart.DashboardController 1.0

Image {
    id: needle
    source: "../images/needle.png" 
    width: 300
    height: 150
    anchors.centerIn: parent
    anchors.horizontalCenterOffset: -250 // move to the left
    anchors.verticalCenterOffset: 30 // move down
    fillMode: Image.PreserveAspectFit
    transformOrigin: Item.Center
    rotation: -150 + (DashboardController.speed / 50 * 180)
}