import pygame
import random
pygame.init()
import time
green = 0,255,0
red = 255,0,0

class Visualization:
    '''
    Main class of the program
    '''
    side_padding = 100
    top_padding = 150
    background_colour  = 247, 202, 201
    block_colour = 146, 168, 209

    font = pygame.font.SysFont("arial",25)
    large_font = pygame.font.SysFont("arial",35)
    def __init__(self,width,height,a_list):
        '''
        initiliaze
        '''
        self.width = width
        self.height = height

        self.screen = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(a_list)

    def set_list(self,a_list):
        '''
        Sets up the block heights, widths, and spacing between
        '''
        self.a_list =a_list
        self.min_value = min(a_list)
        self.max_value = max(a_list)
        
        # Create a spacing of 2 px inbetween
        self.num_spaces = len(a_list) * 2
        self.block_width = round((self.width-self.side_padding-self.num_spaces) / len(a_list))
        
        # Uses the range between the max and the min to show how much
        # taller a certain block needs to be compared to another
        self.block_height = (self.height-self.top_padding) // (self.max_value-self.min_value)

        self.start_x = self.side_padding // 2

    def draw(self, algorithm_name):
        '''
        Draw the screen
        '''

        self.screen.fill(self.background_colour)

        heading = self.large_font.render(algorithm_name,1,self.block_colour)
        self.screen.blit(heading, ((self.width/2-heading.get_width()/2),5))

        controls = self.font.render("Space - Start Sorting Algorithm", 1, self.block_colour)
        self.screen.blit(controls, ((self.width/2-controls.get_width()/2),40))

        algorithms = self.font.render("B - Bubble Sort I - Insertion Sort M - Merge Sort", 1, self.block_colour)
        self.screen.blit(algorithms, ((self.width/2-algorithms.get_width()/2),75))

        self.draw_list()
        pygame.display.update()

    def draw_list(self,colour_pos={}, clear_blocks = False):
        '''
        Draw the list
        '''
        if clear_blocks:
            
            clear_rect = (self.side_padding//2,self.top_padding,self.width-self.side_padding,self.height-self.top_padding)
            pygame.draw.rect(self.screen,self.background_colour,clear_rect)
        
        for i, value in enumerate(self.a_list):
            x = self.start_x+i*(self.block_width+2)
            
            # Added a 1 to the height incase for the case when it is
            # the min value since at that point it will be zero otehrwise
            y= self.height - (value-self.min_value+1)*self.block_height
            
            colour = self.block_colour
            
            # Selecting the blocks that are being moved
            if i in colour_pos:
                colour = colour_pos[i]

            pygame.draw.rect(self.screen,colour,(x,y,self.block_width,self.height-y))

        
        pygame.display.update()

def create_list(length, min_value,max_value):
    '''
    Create the list
    '''
    a_list = []

    for i in range(length):
        a_list.append(random.randint(min_value,max_value))

    return a_list

def bubble_sort(visualizer):
    '''
    Bubble Sort
    '''
    a_list = visualizer.a_list

    for i in range(len(a_list)-1):
        for j in range(len(a_list)-1-i):
            num_1= a_list[j]
            num_2= a_list[j+1]

            if (num_1>num_2):
                a_list[j],a_list[j+1] =a_list[j+1],a_list[j]
                visualizer.draw_list({j:green,j+1:red},True)
                yield True
    return 

def insertion_sort(visualizer):
    '''
    Insertion Sort
    '''
    a_list = visualizer.a_list

    for i in range(1, len(a_list)):
        key = a_list[i]

        j = i-1

        while j>=0 and key< a_list[j]:
            a_list[j+1] = a_list[j]
            j=j-1
            
            visualizer.draw_list({j:green,j+1:red},True)
            yield True
        a_list[j+1] = key

    
        
    return 

def merge_sort(visualizer,a_list,left,right):
    '''
    Merge Sort helper function
    '''
    mid = (left+right) // 2
    if left<right:
        merge_sort(visualizer,a_list,left,mid)
        merge_sort(visualizer,a_list,mid+1,right)
        merge(visualizer,a_list,left,mid,mid+1,right)

def merge(visualizer,a_list,start,mid,mid1,end):
    '''
    Merge sort without splitting into two lists
    '''
    i = start
    j = mid1
    temp_list = []
    
    while i <= mid and j <= end:
        if a_list[i]<a_list[j]:
            temp_list.append(a_list[i])
            i+=1
        else:
            temp_list.append(a_list[j])
            j+=1
    

    # add the rest of i to the end of temp
    while i<= mid:
        temp_list.append(a_list[i])
        i+=1
    # add the rest of j to the end of temp
    while j<= end:
        temp_list.append(a_list[j])
        j+=1
    # set j back to zero to use as the index for temo
    j=0
    for x in range(start,end+1):
        a_list[x] = temp_list[j]
        visualizer.draw_list({x:green,j:red},True)
        j+=1


def main():
    '''
    Run the main program
    '''
    run = True
    clock = pygame.time.Clock()

    length = 100
    min_value = 50
    max_value = 150

    a_list = create_list(length,min_value,max_value)
    visualizer = Visualization(800,600,a_list)

    sorting = False

    merging = False

    sorting_algorithm = insertion_sort
    sorting_algorithm_name = "Insertion Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick()
        if sorting and merging == False:
            try:
                next(sorting_algorithm_generator)
                
            except StopIteration:
                sorting = False
        else:
            visualizer.draw(sorting_algorithm_name)

        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                print("hello")
                sorting_algorithm_generator = sorting_algorithm(visualizer)

            if event.key == pygame.K_m and not sorting:
                sorting = True
                merging = True
                merge_sort(visualizer,visualizer.a_list,0,len(visualizer.a_list)-1)
                sorting_algorithm_name = "MergeSort"
            
            if event.key == pygame.K_b and sorting == False:
                sorting = True
                sorting_algorithm = bubble_sort
                sorting_algorithm_name = "Bubble Sort"
            
            if event.key == pygame.K_i and sorting == False:
                sorting = True
                sorting_algorithm = insertion_sort
                sorting_algorithm_name = "Insetion Sort"

    

    pygame.quit()

if __name__ == "__main__":
    main()