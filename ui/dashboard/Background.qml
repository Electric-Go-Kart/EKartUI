import QtQuick 2.0
import QtQuick.Controls
import org.ekart.DashboardController 1.0

Image {
    id: speedometer
    source: "speedometer9.png"
    anchors.centerIn: parent
}

Image {
    id: needle
    source: "needle.png" 
    width: 10 
    height: 100 
    anchors.bottom: speedometer.verticalCenter
    anchors.horizontalCenter: speedometer.horizontalCenter
    transformOrigin: Item.Bottom
    rotation: DashboardController.speed / 50 * 180 
}
