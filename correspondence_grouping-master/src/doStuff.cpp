//
// Created by duncan on 4/30/19.
//

#include "correspGroup.h"

using namespace N;

int main () {
    CorrespGroup model;
    model.find("../test/milk.pcd", "../test/milk_cartoon_all_small_clorox.pcd");
    return 0;
};