#include <stdio.h>
#include <stdlib.h>
#include <ctype.h> 
#include <string.h>
#include "autocomplete.h"

// struct term{
//     char term[200]; // assume terms are not longer than 200
//     double weight;
// };

int my_compare(const void * a, const void * b){
    struct term *l = (struct term *)a; 
    struct term *r = (struct term *)b;  
    return strcmp(l->term,r->term);
}

int my_compare_2(const void * a, const void * b){
    struct term *l = (struct term *)a; 
    struct term *r = (struct term *)b;  
    return r->weight - l->weight;
}

void read_in_terms(struct term **terms, int *pnterms, char *filename){
    char line[200];
    FILE *fp = fopen(filename, "r");
    if (fp == NULL){
        int some = 0;
        //printf("Failed to open the file\n");
    }else{
        //assign num of terms to *pnterms 
        fgets(line, sizeof(line), fp);
        *pnterms = atoi(line);
        //printf("%d", *pnterms); 

        //assign block of memory to **terms 
        *terms = (struct term *)malloc(sizeof(struct term) * (*pnterms));


        //read in and assign terms to *terms 
        for (int i = 0; i < *pnterms; i++){
            fgets(line, sizeof(line), fp);
            
            //seperate line into weight and term 
            int j = 0;
            char c; 

            for (int m = 0;m < strlen(line);m++){
                c = line[m];

                if (line[m] != ' ' || m > 14){
                    line[j] = line[m];
                    j++;
                }
            }

            line[j] = '\0'; 
            char delim[] = "\t";
            char *str_weight = strtok(line, delim);
            char *str_city_nl = strtok(NULL,delim); 
            char delim_nl[] = "\n"; 
            char *str_city = strtok(str_city_nl, delim_nl); 



            // int j = 0;
            // while(line[j] == ' '){
            //     j++;
            // }
            // int es_1 = j;
            // while (isdigit(line[j]) > 0){
            //     j++;
            // }
            // int ew = j; 
            // while (line[j] == ' '){
            //     j++; 
            // }
            // int es_2 = j;
            // while (line[j] != '\n'){
            //     j++;
            // }
            // int et = j;


            // char str_weight [ew-es_1];
            // char str_city [et-es_2 + 1];
            // //char str_city [strlen(line)-j+1];

            // for (int n = es_1; n < et; n++){
            //     if (n < ew){
            //         str_weight[n-es_1] = line[n];
            //     }

            //     else if (n > es_2){
            //         str_city[n-es_2-1] = line[n];
            //     }
            // }
            // str_weight[ew - es_1] = '\0';
            // str_city[et - es_2] = '\0';
            

            // printf("%s", str_weight);
            // printf("%s", str_city);

            //assign terms to *terms
            strcpy((*terms + i) -> term, str_city); 
            (*terms + i) -> weight = (double)atoll(str_weight); 
        } 

        //sort in lexicographic order using qsort 
        qsort(*terms,*pnterms, sizeof(struct term), my_compare);

        //printf("%f\n", (*terms + 100) -> weight);
        //printf("%s\n", (*terms + 101) -> term);
    }
}

int lowest_match(struct term *terms, int nterms, char *substr){

    int lower = 0;
    int upper = nterms; 
    int index = -1;

    int sublen = strlen(substr);

    while (lower<=upper){
        int mid = (lower + upper) / 2;
        if (strncmp((terms + mid - 1)->term, substr, sublen) == 0){ 
            index = mid; 
            upper = mid - 1;
        }else if (strncmp((terms + mid - 1)->term, substr, sublen) < 0){
            lower = mid + 1; 
        }else if (strncmp((terms + mid - 1)->term, substr, sublen) > 0){
            upper = mid - 1; 
        }
    }

    return index; 
}

int highest_match(struct term *terms, int nterms, char *substr){
    int lower = 0;
    int upper = nterms; 
    int index = -1;

    int sublen = strlen(substr);

    while (lower<=upper){
        int mid = (lower + upper) / 2;
        if (strncmp((terms + mid - 1)->term, substr, sublen) == 0){ 
            index = mid; 
            lower = mid + 1;
        }else if (strncmp((terms + mid - 1)->term, substr, sublen) < 0){
            lower = mid + 1; 
        }else if (strncmp((terms + mid - 1)->term, substr, sublen) > 0){
            upper = mid - 1; 
        }
    }

    return index; 
}

void autocomplete(struct term **answer, int *n_answer, struct term *terms, int nterms, char *substr){
    int low_m = lowest_match(terms, nterms, substr);
    int high_m = highest_match(terms, nterms, substr);


    if (high_m == -1 || low_m == -1){
        *n_answer = 0; 
    }else{
        *n_answer = high_m - low_m + 1;
        *answer = (struct term *)malloc(sizeof(struct term) * (*n_answer));

        for(int i=0;i<*n_answer;i++){
            strcpy((*answer + i) -> term, (terms + low_m + i - 1) -> term);
            (*answer + i) -> weight = (terms + low_m + i - 1) -> weight;  
        }

        //qsort by weight 
        qsort(*answer, *n_answer, sizeof(struct term), my_compare_2);   
    }
}


// int main(void){
//     struct term* terms;
//     int nterms;
//     read_in_terms(&terms, &nterms, "cities.txt");
//     //printf("%d", strcmp("Me", "Ka"));

//     // printf("%s\n", (terms + 1500)->term);
//     // printf("%f\n", (terms + 1500)->weight);

  
//     //printf("%i", lowest_match(terms, nterms, "Tor"));
//     //int num = lowest_match(terms, nterms, "Tor");
//     //printf("%s\n", (terms + num - 1)->term);
//     //printf("%f\n", (terms + num - 1)->weight);

//     // int num_1 = highest_match(terms, nterms, "Tor");
//     // printf("%s", (terms + num_1 - 1)->term);

//     struct term *answer;
//     int n_answer;
//     autocomplete(&answer, &n_answer, terms, nterms, "Kinshasa, Democratic Republic of the Congo");
//     printf("%s\n", (answer)->term);
//     printf("%f", (answer)->weight);
    
//     return 0; 
// }