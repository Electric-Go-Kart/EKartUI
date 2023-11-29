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
    let zeroAngle = 210; // Angle at 0 MPH
    let maxAngle = 90; // Angle at max speed (50 MPH for example)
    let range = zeroAngle - maxAngle; // Total range of motion
    rotation: zeroAngle - (DashboardController.speed / 50 * range)
}