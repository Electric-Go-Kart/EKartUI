import QtQuick
import QtQuick.Controls
import org.ekart.DashboardController 1.0

Image {
    id: needle
    source: "needle.png" 
    width: 10 
    height: 100 
    rotation: DashboardController.speed / 50 * 180 
}