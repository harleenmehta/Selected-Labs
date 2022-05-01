#include "seamcarving.h"
#include "c_img.h"
#include <math.h>
#include <stdlib.h>
#include <stdio.h>


void calc_energy(struct rgb_img *im, struct rgb_img **grad){
    
    int height = im->height;
    int width = im->width;
    (*grad) = (struct rgb_img *)malloc(sizeof(struct rgb_img));
    (*grad)->raster = (uint8_t *)malloc(3 * height * width);
    (*grad)->height = height;
    (*grad)->width = width;

    int Rx, Gx, Bx, Ry, Gy, By;

    for (int y = 0; y < im->height; y++){
        
        for (int x = 0; x < im->width; x++){

            if (x == 0){
                Rx = get_pixel(im, y, x+1, 0) - get_pixel(im, y, im->width - 1, 0);
                Gx = get_pixel(im, y, x+1, 1) - get_pixel(im, y, im->width - 1, 1);
                Bx = get_pixel(im, y, x+1, 2) - get_pixel(im, y, im->width - 1, 2);

                

            } else if (x == im->width - 1){
                Rx = get_pixel(im, y, 0, 0) - get_pixel(im, y, x - 1, 0);
                Gx = get_pixel(im, y, 0, 1) - get_pixel(im, y, x - 1, 1);
                Bx = get_pixel(im, y, 0, 2) - get_pixel(im, y, x - 1, 2);
            } else {
                Rx = get_pixel(im, y, x + 1, 0) - get_pixel(im, y, x - 1, 0);
                Gx = get_pixel(im, y, x + 1, 1) - get_pixel(im, y, x - 1, 1);
                Bx = get_pixel(im, y, x + 1, 2) - get_pixel(im, y, x - 1, 2);
            }

             if (y == 0){
                 Ry = get_pixel(im, y + 1, x, 0) - get_pixel(im, im->height - 1, x, 0);
                Gy = get_pixel(im, y + 1, x, 1) - get_pixel(im, im->height - 1, x, 1);
                 By = get_pixel(im, y + 1, x, 2) - get_pixel(im, im->height - 1, x, 2);

             } else if (y == im->height - 1){
                 Ry = get_pixel(im, 0, x, 0) - get_pixel(im, y - 1, x, 0);
                 Gy = get_pixel(im, 0, x, 1) - get_pixel(im, y - 1, x, 1);
                 By = get_pixel(im, 0, x, 2) - get_pixel(im, y - 1, x, 2);
             } else {
                 Ry = get_pixel(im, y + 1, x, 0) - get_pixel(im, y - 1, x, 0);
                 Gy = get_pixel(im, y + 1, x, 1) - get_pixel(im, y - 1, x, 1);
                By = get_pixel(im, y + 1, x, 2) - get_pixel(im, y - 1, x, 2);
             }

            
            double Dx = pow((double)Rx, 2) + pow((double)Gx, 2) + pow((double)Bx, 2);
            double Dy = pow((double)Ry, 2) + pow((double)Gy, 2) + pow((double)By, 2);
            double energy = sqrt(Dx + Dy);

            
            uint8_t dg_energy = (uint8_t)(energy/10);





            ((*grad)->raster)[3 * (y*(im->width) + x) + 0] = dg_energy;
            (*grad)->raster[3 * (y*(im->width) + x) + 1] = dg_energy;
            ((*grad)->raster)[3 * (y*(im->width) + x) + 2] = dg_energy;
            
        }
    }

}

    double min3(double a, double b, double c){
        if (a < b && a < c){
            return a;
        } else if (b < c){
            return b;
        } else {
            return c;
        }
    }

    double min2(double a, double b){
        if (a < b){
            return a;
        } else {
            return b;
        }
    }

    void dynamic_seam(struct rgb_img *grad, double **best_arr){
        int height = grad->height;
        int width = grad->width;

        *best_arr = (double *)malloc(height * width * (sizeof(double)));

        for(int y = 0; y < height; y++){
            for(int x = 0; x < width; x++){
                if (y==0){
                    (*best_arr)[y * width + x] = get_pixel(grad, y, x, 0);
                } else{
                    if (x==0){
                        (*best_arr)[y * width + x] = get_pixel(grad, y, x, 0) + min2((*best_arr)[(y-1) * width + x],(*best_arr)[(y-1) * width + x + 1]);
                    }else if (x== width - 1){
                        (*best_arr)[y * width + x] = get_pixel(grad, y, x, 0) + min2((*best_arr)[(y-1) * width + x],(*best_arr)[(y-1) * width + x - 1]);
                    }else {
                        (*best_arr)[y * width + x] = get_pixel(grad, y, x, 0) + min3((*best_arr)[(y-1) * width + x],(*best_arr)[(y-1) * width + x - 1],(*best_arr)[(y-1) * width + x + 1]);
                    }
                }


            }
        }
        // for(int y = 0; y < height; y++){
        //     printf("\n");
        //     for(int x = 0; x < width; x++){
        //         printf("%f     ", (*best_arr)[y * width + x]);

        //     }
        // }


}

void recover_path(double *best, int height, int width, int **path){
    *path = (int *)malloc(height * (sizeof(int)));

    double cur_min = best[(height - 1)*width];
    int min_index = 0;
        for (int x = 0; x < width; x++){
            if (best[(height - 1)*width + x] < cur_min){
                cur_min = best[(height - 1)*width + x];
                min_index = x;
            }
        }

        *(*path + height - 1 )= min_index;

    
    int y = height - 2;

    while(y>=0){
        int cur_min_index;
        if (*(*path + y + 1) == 0){
            if (best[y*width + 0] <= best[y*width + 1]){
                cur_min_index = 0;
            } else {
                cur_min_index = 1;
            }

        }else if (*(*path + y + 1) == width - 1){
            if (best[y*width + width - 2] <= best[y*width + width - 1]){
                cur_min_index = width - 2;
            } else {
                cur_min_index = width - 1;
            }

        }else {
            if (best[y*width + *(*path + y + 1) - 1] <= best[y*width + *(*path + y + 1)] && best[y*width + *(*path + y + 1) - 1] <= best[y*width + *(*path + y + 1) + 1]){
                cur_min_index = *(*path + y + 1) - 1;
            } else if (best[y*width + *(*path + y + 1)] <= best[y*width + *(*path + y + 1) + 1]){
                cur_min_index = *(*path + y + 1);
            } else{
                cur_min_index = *(*path + y + 1) + 1;
            }
        }
        *(*path + y) = cur_min_index;
        y--;
    }

    // printf("\n\n");
    // for(int i = 0; i < height; i++ ){
    //     printf("%d  ", *(*path + i));
    // }
    // printf("\n");
}

void remove_seam(struct rgb_img *src, struct rgb_img **dest, int *path){
    int height = src->height;
    int width = src->width;

    (*dest) = (struct rgb_img *)malloc(sizeof(struct rgb_img));
    (*dest)->raster = (uint8_t *)malloc(3 * height * (width-1));
    (*dest)->height = height;
    (*dest)->width = width - 1;
    
    for(int y = 0; y < height; y++){
        int removed = 0;
        int to_remove = *(path + y);
        for(int x = 0; x < width; x++){
            if (x != to_remove){
                if(removed){
                    ((*dest)->raster)[3 * (y*(src->width - 1) + x - 1) + 0] = src->raster [3 * (y*(src->width) + x) + 0];
                    ((*dest)->raster)[3 * (y*(src->width - 1) + x - 1) + 1] = src->raster [3 * (y*(src->width) + x) + 1];
                    ((*dest)->raster)[3 * (y*(src->width - 1) + x - 1) + 2] = src->raster [3 * (y*(src->width) + x) + 2];


                }else{
                    ((*dest)->raster)[3 * (y*(src->width - 1) + x) + 0] = src->raster [3 * (y*(src->width) + x) + 0];
                    ((*dest)->raster)[3 * (y*(src->width - 1) + x) + 1] = src->raster [3 * (y*(src->width) + x) + 1];
                    ((*dest)->raster)[3 * (y*(src->width - 1) + x) + 2] = src->raster [3 * (y*(src->width) + x) + 2];

                }

            }else{
                removed = 1;
            }
        } 

        }
    }



