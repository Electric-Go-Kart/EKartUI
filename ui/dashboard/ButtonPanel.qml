import QtQuick
//import QtQuick.Timeline
import QtQuick.Controls
import org.ekart.DashboardController 1.0

Rectangle {
    id: buttonPanel
    readonly property int buttonSize: 80
    readonly property int buttonRadius: 15
    readonly property int outerMargin: 10
    readonly property int innerMargin: 5

    
    width: 790
    height: parent.height
    color: "#44444400"
    anchors.centerIn: parent

	//Lights Toggle
	Button {
		id: lights
		text: "Lights"
		anchors.top: camera.bottom
        anchors.right: parent.right
        anchors.topMargin: outerMargin
        anchors.rightMargin: outerMargin
		font.family: "Haettenschweiler"
		font.pixelSize: 22
		hoverEnabled: false
		onClicked: {
			DashboardController.toggleHeadlight()
			checked = !checked
		}

		background: Rectangle {
			implicitWidth: buttonSize
			implicitHeight: buttonSize
			border.color: "#1a1a1a"
			border.width: 4
			radius: buttonRadius
			color: parent.checked ? "#ffb0b0" : "#f2f2f2"
		}
	}

	//Camera Button
	Button {
		id: camera
		text: "Camera"
		width: buttonSize
		anchors.top: parent.top
        anchors.right: parent.right
        anchors.topMargin: outerMargin
        anchors.rightMargin: outerMargin
		font.family: "Haettenschweiler"
		font.pixelSize: 22
		hoverEnabled: false
		onClicked: stateGroup.state = "camera"

		background: Rectangle {
			implicitWidth: buttonSize
			implicitHeight: buttonSize
			border.color: "#1a1a1a"
			border.width: 4
			radius: buttonRadius
			color: parent.down ? "#c0c0c0" : "#f2f2f2"
		}
	}

	Button {
    id: shutdownButton
    text: "Shutdown"
	width: buttonSize
    anchors.top: parent.top
    anchors.right: camera.left
    anchors.topMargin: outerMargin
    anchors.rightMargin: outerMargin
    font.family: "Haettenschweiler"
    font.pixelSize: 22
    hoverEnabled: false
    onClicked: shutdownDialog.open()
    background: Rectangle {
        implicitWidth: buttonSize
        implicitHeight: buttonSize
        border.color: "#1a1a1a"
        border.width: 4
        radius: buttonRadius
        color: parent.down ? "#c0c0c0" : "#f2f2f2"
    	}
	}

	Button {
		id: reverse
		width: buttonSize
		anchors.centerIn: parent
		anchors.verticalCenterOffset: 10
		font.family: "Haettenschweiler"
		font.pixelSize: 22
		hoverEnabled: false
		onClicked: gpioController.setLow()

		background: Image {
			source: "../images/arrow.png"
			anchors.fill: parent
			rotation: 180
			fillMode: Image.PreserveAspectFit
		}
	}

	Button {
		id: forward
		width: buttonSize
		anchors.centerIn: parent
		anchors.verticalCenterOffset: -40
		font.family: "Haettenschweiler"
		font.pixelSize: 22
		hoverEnabled: false
		onClicked: gpioController.setHigh()

		background: Image {
			source: "../images/arrow.png"
			anchors.fill: parent
			fillMode: Image.PreserveAspectFit
		}
	}

	Dialog {
    id: shutdownDialog
    title: "Confirm Shutdown"
    modal: true
    standardButtons: Dialog.Yes | Dialog.No

    onAccepted: {
        DashboardController.shutdownSystem()
    }

    Text {
        text: "Are you sure you want to shutdown the system?"
        anchors.centerIn: parent
    	}
	}

	//Settings Button
	//Button {
	//	id: settings
	//	text: "Info"
	//	anchors.top: parent.top
    //    anchors.left: parent.left
    //  anchors.topMargin: outerMargin
	//	implicitWidth: DashboardController.parked ? buttonSize : 183
	//	implicitHeight: buttonSize
	//	font.family: "Haettenschweiler"
	//	font.pixelSize: 17
	//	hoverEnabled: false
	//	onClicked: {
	//		DashboardController.state = "info"
	//	}

	//	background: Rectangle {
	//		anchors.fill: parent
	//		border.color: "#1a1a1a"
	//		border.width: 4
	//		radius: buttonRadius
	//		color: parent.down ? "#c0c0c0" : "#f2f2f2"
	//	}
	//}

	//Settings Button
	//Button {
	//	id: lock
	//	text: DashboardController.locked ? "Unlock" : "Lock"
	//	checked: DashboardController.locked
	//	width: buttonSize
	//	anchors.top: parent.top
    //    anchors.left: parent.left
    //    anchors.topMargin: outerMargin
    //    anchors.rightMargin: outerMargin
	//	font.family: "Haettenschweiler"
	//	font.pixelSize: 22
	//	hoverEnabled: false
	//	onClicked: {
	//		if(checked) DashboardController.state = "default"
	//		else DashboardController.state = "locked"
	//	}

	//	background: Rectangle {
	//		implicitWidth: buttonSize
	//		implicitHeight: buttonSize
	//		border.color: "#1a1a1a"
	//		border.width: 4
	//		radius: buttonRadius
	//		color: parent.checked ? "#ffb0b0" : "#f2f2f2"
	//	}
	//}

	//Back Button
	//Button {
	//	id: back
	//	text: "Back"
	//	anchors.top: camera.bottom
	//	anchors.left: parent.left
	//	anchors.right: parent.right
	//	anchors.topMargin: innerMargin
	//	anchors.leftMargin: outerMargin
	//	anchors.rightMargin: outerMargin
	//	font.family: "Haettenschweiler"
	//	font.pixelSize: 22
	//	hoverEnabled: false
	//	onClicked: DashboardController.state = "default"

	//		background: Rectangle {
	//		implicitWidth: buttonSize
	//		implicitHeight: buttonSize
	//		border.color: "#1a1a1a"
	//		border.width: 4
	//		radius: buttonRadius
	//		color: parent.down ? "#c0c0c0" : "#f2f2f2"
	//	}
	//}

	//States & Transitions
	StateGroup {
		id: buttonStateGroup
		state: DashboardController.state
		states: [
			State {
				name: "default"
				PropertyChanges {
					target: settings
					visible: true
				}
				PropertyChanges {target: back; visible: false}
				PropertyChanges {
					target: lock 
					visible: DashboardController.parked
					anchors.right: settings.left
					anchors.rightMargin: innerMargin
				}
			},
			State {
				name: "settings"
				PropertyChanges {target: settings; visible: false}
				PropertyChanges {target: back; visible: true}
				PropertyChanges {
					target: lock
					visible: false
					anchors.right: parent.right
				}
			},
			State {
				name: "info"
				PropertyChanges {target: settings; visible: false}
    				PropertyChanges {target: back; visible: true}
    				PropertyChanges {
        				target: lock
        				visible: false
        				anchors.right: parent.right
    				}
			},
			State {
				name: "locked"
				PropertyChanges {target: settings; visible: false}
				PropertyChanges {target: back; visible: false}
				PropertyChanges {
					target: lock
					visible: true
					anchors.right: parent.right
					anchors.rightMargin: outerMargin
				}
			}
		]
	}
}
