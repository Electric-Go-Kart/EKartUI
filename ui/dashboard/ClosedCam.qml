import QtQuick
//import QtQuick.Timeline
import QtQuick.Controls
import org.ekart.DashboardController 1.0

Button {
		id: closecamera
		text: "Close Camera"
		width: 80
        height: 80
        anchors.verticalCenter: parent.verticalCenter
		font.family: "Haettenschweiler"
		font.pixelSize: 22
		hoverEnabled: false
		onClicked: stateGroup.state = "default"

		background: Rectangle {
			implicitWidth: buttonSize
			implicitHeight: buttonSize
			border.color: "#1a1a1a"
			border.width: 4
			radius: buttonRadius
			color: parent.down ? "#c0c0c0" : "#f2f2f2"
	}
}