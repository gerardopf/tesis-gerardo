%% Conexión al Robotat
robotat = robotat_connect()

%% Obtener pose de markers
clc

% FALTAN MARKERS 1 Y 9
markers = [2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22];
poses = robotat_get_pose(robotat, markers, 'eulzyx')

marker_offsets = poses(:,4)

% Aplicar desfases
for i=1:length(markers)
    poses(i,4) = poses(i,4) - marker_offsets(i);
end

% mostrar nuevas poses
disp(poses)

% Ver markers
robotat_trvisualize(robotat, markers)
% x rojo
% y azul
% z verde

%% Desconexión del Robotat y Pololu 3pi
robotat_disconnect(robotat);