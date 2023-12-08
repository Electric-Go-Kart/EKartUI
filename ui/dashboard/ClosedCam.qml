import QtQuick
//import QtQuick.Timeline
import QtQuick.Controls
import org.ekart.DashboardController 1.0



Button {
		id: closecamera
		text: "Close Camera"
		width: 150
        height: 20
        anchors.verticalCenter: parent.verticalCenter
        anchors.top: parent.top
		font.family: "Haettenschweiler"
		font.pixelSize: 22
		hoverEnabled: false
		onClicked: stateGroup.state = "default"

		background: Rectangle {
			implicitWidth: 150
			implicitHeight: 150
			border.color: "#1a1a1a"
			border.width: 4
			radius: 15
			color: parent.down ? "#c0c0c0" : "#f2f2f2"
	}
}