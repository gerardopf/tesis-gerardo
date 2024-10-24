markers = [22,21,20,3,4,5,15];

robotat = robotat_connect();

pose = robotat_get_pose(robotat, markers,'eulzyx')

robotat_trvisualize(robotat,markers)