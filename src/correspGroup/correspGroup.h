//
// Created by duncan on 4/30/19.
//

#include <iostream>

#ifndef CORRESPONSEGROUPING_CORRESPGROUP_H
#define CORRESPONSEGROUPING_CORRESPGROUP_H

namespace N {
    class CorrespGroup {
    public:
        void find (std::string model_filename_, std::string scene_filename_);
    };

    class Foo{
    public:
        void bar(){
            std::cout << "Hello" << std::endl;
        }
    };


}


extern "C" {
    Foo* Foo_new(){ return new Foo(); }
    void Foo_bar(Foo* foo){ foo->bar(); }
}

#endif //CORRESPONSEGROUPING_CORRESPGROUP_H
