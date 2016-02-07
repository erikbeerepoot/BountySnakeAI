%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%% Battlesnake.io simple simulation  %%%%%
%%%%%% Randomly puts a few snakes on a   %%%%% 
%%%%%% board of a randomly generated si- %%%%% 
%%%%%% ze and attempts to solve          %%%%% 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function result = sim()
    disp('Battlesnake greedy sim')

    %Randomly generate size
    a = 10;
    b = 20;
    m = round(a + (b-a).*rand(1));
    n = round(a + (b-a).*rand(1));

    %Start with empty board, B
    B = zeros(m,n);

    %Game parameters
    snakeLength = 4;
    numSnakes = 3;
    assert(mod(numSnakes,2)==0,'Number of snakes must be even')
    
    
    
    
%     
%     %Randomly pick starting positions
%     startLocations = zeros(numSnakes,2)
%     for idx = 1 : numSnakes
%         [x,y] = generateStartLocations(m,n)
%        startLocations(idx,:) = [x,y]
%     end
%     
%     %Randomly pick tail locations (observing length constraint)
%     startLocations = zeros(numSnakes,2)
%     for idx = 1 : numSnakes
%         [x0,y0] = startLocations(idx,:)
%         [x,y] = generateStartLocations(x0-snakeLength,x0+snakeLength)
%        startLocations(idx,:) = [x,y]
%     end
end

function result = uniformRandomInt(a,b)
    result = round(a + (b-a).*rand(1));
end

function [x,y] = generateStartLocations(m,n)
    x = uniformRandomInt(0,n);
    y = uniformRandomInt(0,m);
end