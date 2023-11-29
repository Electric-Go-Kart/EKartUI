import QtQuick
import QtQuick.Controls
import org.ekart.DashboardController 1.0

Image {
    id: needle
    source: "../images/needle.png" 
    width: 200 
    height: 100
    anchors.centerIn: parent
    fillMode: Image.PreserveAspectFit
    rotation: DashboardController.speed / 50 * 180 
}