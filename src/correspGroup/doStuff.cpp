//
// Created by duncan on 4/30/19.
//

#include "correspGroup.h"

using namespace N;

int main () {
    CorrespGroup model;

    // pull information from the http server
    // save the scene mesh to pcd

    model.find("../test/milk.pcd", "../test/milk_cartoon_all_small_clorox.pcd");
    // change the function to return a string
    // send string to http server

    return 0;
};