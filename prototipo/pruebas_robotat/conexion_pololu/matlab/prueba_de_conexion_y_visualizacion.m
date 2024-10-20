markers = [7,8,10,11,12,13,21];

robotat = robotat_connect();

pose = robotat_get_pose(robotat, markers,'eulzyx')

robotat_trvisualize(robotat,markers)