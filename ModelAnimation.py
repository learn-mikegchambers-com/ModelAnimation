from PIL import Image, ImageDraw, ImageFont
import imageio

class ModelAnimation():

    def map_range_int(self, input_list, new_range): # a: input list, b: map range, c: value
        a = (max(input_list) , min(input_list))
        b = new_range
        (a1, a2), (b1, b2) = a, b
        output_list = []
        for s in input_list:
            if (a2 - a1) != 0.0:
                v = (b1 + ((s - a1) * (b2 - b1) / (a2 - a1)))
            else: 
                v = new_range[1]
            output_list.append(int(v))
        return output_list


    def create_animation(self, model_weights, input_size, **kwargs):
        
        # Layout and size...
        layout_margin         = kwargs['margin']               if ('margin' in kwargs)               else 200
        layout_size           = kwargs['size']                 if ('size' in kwargs)                 else [1920, 1080]
        layout_node_size      = kwargs['node_size']            if ('node_size' in kwargs)            else 90
        layout_node_layer_gap = kwargs['node_gap']             if ('node_gap' in kwargs)             else 40
        
        # Colors and widths...
        background_color      = kwargs['background_rgba']      if ('background_rgba' in kwargs)      else (32, 32, 32, 0)
        node_base_color       = kwargs['node_rgb']             if ('node_rgb' in kwargs)             else (248, 167, 3)
        node_stroke_width     = kwargs['node_stroke']          if ('node_stroke' in kwargs)          else 5
        conn_base_color       = kwargs['conn_rgb']             if ('conn_rgb' in kwargs)             else (81, 181, 237)
        conn_max_width        = kwargs['conn_max_width']       if ('conn_max_width' in kwargs)       else 20
        
        # Frame numbers...
        frame_numbers         = kwargs['frame_numbers']        if ('frame_numbers' in kwargs)        else False
        frame_numbers_title   = kwargs['frame_numbers_title']  if ('frame_numbers_title' in kwargs)  else 'epoch'
        frame_numbers_font    = kwargs['frame_numbers_font']   if ('frame_numbers_font' in kwargs)   else 'OpenSans-Regular.ttf'
        frame_numbers_size    = kwargs['frame_numbers_size']   if ('frame_numbers_size' in kwargs)   else 50
        frame_numbers_xy      = kwargs['frame_numbers_xy']     if ('frame_numbers_xy' in kwargs)     else (100,100)
        frame_numbers_rgb     = kwargs['frame_numbers_rgb']    if ('frame_numbers_rgb' in kwargs)    else (50,50,50)
        
        # Animated GIF...
        output_animation      = kwargs['gif']                  if ('gif' in kwargs)                  else False
        output_name           = kwargs['gif_name']             if ('gif_name' in kwargs)             else 'animation.gif'
        output_fps            = kwargs['fps']                  if ('fps' in kwargs)                  else (5)
        
        print("Starting to render frames...")

        image_list = []

        ###############################################################################
        # Main loop, loops through all the 'frames' (or maybe epochs) of data:

        for frames in range(len(model_weights)):

            print('.', end ="")
            
            ###############################################################################
            # Within this frame, get the nodes and the connections (bias and weights):

            nodes = model_weights[frames][1::2]
            
            input_node_size = 1
            for i in input_size:
                if isinstance(i, int):
                    input_node_size = input_node_size * i
            
            nodes.insert(0, [0] * input_node_size)
            
            connections = model_weights[frames][0::2]

            ###############################################################################
            # Create the layers to draw into:

            im_nodes       = Image.new('RGBA', (layout_size[0], layout_size[1]), (255, 255, 255, 0))
            im_nodes_back  = Image.new('RGBA', (layout_size[0], layout_size[1]), (255, 255, 255, 0))
            im_connections = Image.new('RGBA', (layout_size[0], layout_size[1]), background_color)

            draw_nodes       = ImageDraw.Draw(im_nodes) 
            draw_nodes_back  = ImageDraw.Draw(im_nodes_back) 
            draw_connections = ImageDraw.Draw(im_connections) 

            cols = ((layout_size[0] - (2*layout_margin)) / (len(nodes)-1)) - (layout_node_size/2)

            prv_nodes = []

            ###############################################################################
            # Draw the nodes:

            for i in range(len(nodes)):

                layer_height = (len(nodes[i]) * (layout_node_size + layout_node_layer_gap))
                layer_top = (layout_size[1] - layer_height)/2

                curr_nodes = []

                for o in range(len(nodes[i])):

                    node_colors_a = self.map_range_int(nodes[i],(255,0))

                    node_pos_x = layout_margin + (i * cols)
                    node_pos_y = layer_top + (o * (layout_node_size + layout_node_layer_gap))

                    # Draw a the background for the node... 
                    draw_nodes_back.ellipse((node_pos_x, node_pos_y, 
                                        node_pos_x+layout_node_size, 
                                        node_pos_y+layout_node_size), 
                                       fill=(background_color[0],
                                             background_color[1],
                                             background_color[2],
                                             255))
            
                    # Draw the node on the background...
                    draw_nodes.ellipse((node_pos_x, node_pos_y, 
                                        node_pos_x+layout_node_size, 
                                        node_pos_y+layout_node_size), 
                                       fill=(node_base_color[0],
                                             node_base_color[1], 
                                             node_base_color[2],
                                             node_colors_a[o]
                                            ),
                                       outline=node_base_color, 
                                       width=node_stroke_width)

                    curr_nodes.append([node_pos_x,node_pos_y])


                ###############################################################################
                # Draw the connection lines:

                node_offset = layout_node_size / 2
                
                if len(prv_nodes) > 0:

                    for pni in range(len(prv_nodes)):
                        
                        connection_widths = self.map_range_int(connections[i-1][pni],(conn_max_width,0))
                        connection_colors_r, connection_colors_g, connection_colors_b = conn_base_color
                        connection_oppacity = 255

                        for cni in range(len(curr_nodes)):
                                                   
                            pn = prv_nodes[pni]
                            cn = curr_nodes[cni]
                            
                            if connection_widths[cni] > 0:
                            
                                draw_connections.line((pn[0]+node_offset, 
                                                       pn[1]+node_offset, 
                                                       cn[0]+node_offset, 
                                                       cn[1]+node_offset), 
                                                      fill=(connection_colors_r,
                                                            connection_colors_g, 
                                                            connection_colors_b,
                                                            connection_oppacity),
                                                      width=connection_widths[cni])

                prv_nodes = curr_nodes

                
            ###############################################################################
            # Write the frame counters:

            if frame_numbers:
                font = ImageFont.truetype(frame_numbers_font, frame_numbers_size)
                draw_nodes.text(frame_numbers_xy,frame_numbers_title + ": " + str(frames), frame_numbers_rgb,font=font)

            ###############################################################################
            # Combine the layers together:
            
            im_connections.paste(im_nodes_back, (0, 0), im_nodes_back)
            im_connections.paste(im_nodes, (0, 0), im_nodes)
            im_name = str(frames) + ".png"
            im_connections.save(im_name)
            image_list.append(im_name)

        ###############################################################################
        # Build the aniimated GIF:

        if output_animation:
        
            print("\nBuilding animation...")

            images = []
            for filename in image_list:
                images.append(imageio.imread(filename))
                print('.', end ="")
            
            imageio.mimsave(output_name, images, fps=output_fps)

            print("\nAnimation saved to:", output_name)
            

