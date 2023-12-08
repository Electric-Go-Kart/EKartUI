import QtQuick
//import QtQuick.Timeline
import QtQuick.Controls
import org.ekart.DashboardController 1.0

Button {
		id: closecamera
		text: "Close Camera"
		width: buttonSize
		anchors.top: parent.top
        anchors.right: parent.right
        anchors.topMargin: outerMargin
        anchors.rightMargin: outerMargin
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