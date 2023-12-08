import QtQuick
//import QtQuick.Timeline
import QtQuick.Controls
import org.ekart.APDView 1.0


Item {
	anchors.fill: parent

	//Camera View
	APDView {
		id: apdView
		anchors.horizontalCenter: parent.horizontalCenter
		implicitWidth: 640
		implicitHeight: 480
		visible: false
	}

	//Button panel
	ButtonPanel {
		id: buttonPanel
	}

	Background {
		id: background
		anchors.horizontalCenter: parent.horizontalCenter
	}

	//CenterPanel {
	//	id: centerpanel
	//	anchors.horizontalCenter: parent.horizontalCenter
	//}

	//Info panel
	//InfoPanel {
	//	id: infoPanel
	//	anchors.verticalCenter: parent.verticalCenter
	//}
/*
	//Regenerative braking panel
	RegenPanel {
		id: regenPanel
		anchors.bottom: parent.bottom
		anchors.horizontalCenter: parent.horizontalCenter
	}
*/

	//Battery charge panel
	BatteryPanel {
		id: batteryPanel
		x: 198
		anchors.bottom: parent.bottom
	}

	//Tachometer
	//Tachometer {
	//	id: tachometer
	//}
	
	Needle {
		id: needle
		anchors.fill: parent.horizontalCenter
	}

	//States & Transitions
	StateGroup {
		id: stateGroup
		state: "default"
		states: [
			State {
				name: "default"
				PropertyChanges {
					target: apdView
				}
				//PropertyChanges {
				//	target: centerpanel
				//	open: true
				//	y: 0
				//}
				PropertyChanges {target: buttonPanel; x: 597}
				//PropertyChanges {target: tachometer; x: 560; y: 253}
				//PropertyChanges {target: infoPanel; x: 0}
				PropertyChanges {target: batteryPanel; anchors.bottomMargin: 0}
			},
			State {
				name: "camera"
				PropertyChanges {
					target: apdView
					visible: true
				}
				//PropertyChanges {
				//	target: centerpanel
				//	open: false
				//	y: -350
				//}
				PropertyChanges {target: buttonPanel; x: 800}
				//PropertyChanges {target: tachometer; x: 770; y: 450}
				//PropertyChanges {target: infoPanel; x: -240}
				PropertyChanges {target: batteryPanel; anchors.bottomMargin: -56}
			}
		]
		
		transitions: [
			Transition {
				from: "default"
   				to: "camera"
    			SequentialAnimation {
        			PropertyAnimation {
            			target: apdView
            			property: "opacity"
            			from: 0
            			to: 1
            			duration: 150
        }
					//PropertyAnimation {
					//	target: centerpanel
					//	property: "y"
					//	duration: 150
					//}
					//PropertyAnimation {
					//	target: infoPanel
					//	property: "x"
					//	duration: 150
					//}
					PropertyAnimation {
						target: buttonPanel
						property: "x"
						duration: 150
					}
					// PropertyAnimation {
					// 	target: tachometer
					// 	property: "x"
					// 	duration: 150
					// }
					// PropertyAnimation {
					// 	target: tachometer
					// 	property: "y"
					// 	duration: 150
					// }
					PropertyAnimation {
						target: batteryPanel
						property: "anchors.bottomMargin"
						duration: 150
					}
				}
				to: "*"
				from: "*"
			}
		]
	}
}
