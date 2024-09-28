markers = [22,12,19,7,5,8];

robotat = robotat_connect();

pose = robotat_get_pose(robotat, markers,'quat');

robotat_trvisualize(robotat,markers)
