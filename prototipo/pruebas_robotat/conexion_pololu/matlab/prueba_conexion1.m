markers = [4,5,10];

robotat = robotat_connect();

pose = robotat_get_pose(robotat, markers,'quat');

robotat_trvisualize(robotat,markers)
